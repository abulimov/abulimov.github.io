---
title: "Snooping on unix domain sockets traffic"
date: 2021-12-02
slug: unix-socket-snoop
Categories: [IT]
tags: [BPF, Linux, Python]
---

I often work with various binary protocol, with majority of work being implementing those protocols in Go or Rust.

And when dealing with such tasks, I find it extremely useful to be able to snoop on
the traffic between existing/reference implementations.

When communication happens over network (even locally), it's easy - just fire up some
good old `tcpdump` and then maybe analyze the dump with Wireshark.

But what if communication happens over the [Unix domain sockets](https://man7.org/linux/man-pages/man7/unix.7.html)?

Then things become tricky, especially if we want to capture this traffic passively.

## Available solutions

Let's explore the options we have, starting from simplest ones.

### Reconfigure the reference implementation to use network

Of course, the easiest approach would be to just tell the app to use network instead of Unix socket.
If there is a flag/config option to do so - great, we are done here!

But often the software deliberately makes some things accessible only over the Unix sockets, mostly for security reasons.

For example, [chrony](https://chrony.tuxfamily.org/) NTP daemon allows certain management protocol packets only over the Unix socket,
which has permissions set in a way that unprivileged user won't even be able to access it.

### socat

It's often possible to have `socat` set up the socket and dump everything that gets sent to it, or redirect it to network.

For example, here is what might be used to snoop on some process and send it's traffic to network, where it could be dumped by `tpcdump`.
```
sudo socat -v UNIX-LISTEN:/path/to/some.sock,fork TCP-CONNECT:127.0.0.1:8090
```

However, this action is disruptive to the running processes, and I personally never had success with this approach.

### strace

It is of course possible to see what is being sent to the socket using any form of syscall tracing.
In fact, that was my go-to approach before I did my research and found better ways to do it.

Here is how one can see what `chronyc` sends to `chronyd` over the socket when asked for 'ntpdata'
```
> sudo strace -xx -e sendto,recvfrom -v -s 10000 chronyc ntpdata
sendto(3, "\x06\x01\x00\x00\x00\x0e\x00\x00\x02\x48\x5c\x29\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", 32, 0, NULL, 0) = 32
...
```

Again, the problem here is that it's disruptive and requires changing how the reference app is being run.
And of course if the app does more communication with same syscall, like `sendto` in chronyc example -
we'll have to sift through all of the messages based on file descriptors.

So this approach works well enough, but we can do better!

### bpftrace

Now we are getting to the truly passive solutions (although they are Linux-specific),
thanks to the amazing power of [BPF](https://www.kernel.org/doc/html/latest/bpf/index.html).

For example, we can snoop on same `sendto` syscall via `bpftrace`, which uses BPF with kernel tracepoints:
```
> sudo bpftrace -e 'tracepoint:syscalls:sys_enter_sendto /comm == "chronyc"/ {printf("%r\n", buf(args->buff, args->len));}'
\x06\x01\x00\x00\x00\x0e\x00\x00\x02\x48\x5c\x29\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
...
```

This is pretty neat, but we still need to know exactly what syscall is used to send data over the socket.

### sockdump.py

Finally, if we dig more into how the Unix sockets are done in Linux kernel, we can hook *kprobe* to kernel
functions like `unix_stream_sendmsg` and capture everything regardless of the method the app uses to send data to the socket.

This is exactly what nifty script called [`sockdump`](https://github.com/mechpen/sockdump) does under the hood!

I find this tool extremely useful, and recently [contributed to it](https://github.com/mechpen/sockdump/pull/8)
support for DGRAM sockets and dumping data in escaped hex string format,
which can be then used directly in Go or Python as for example an input for unittests.

Here is how it looks like for `pmc` talking to `ptp4l` (both are part of [linuxptp](http://linuxptp.sourceforge.net) project):

```
$ sudo ./sockdump.py '/var/run/p*' --format hexstring
waiting for data
10:11:28.968 >>> process pmc [1108317 -> 0] len 74(74)
\x0d\x12\x00\x4a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe9\x5d\x00\x00\x04\x7f\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x01\x00\x16\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
10:11:28.968 >>> process ptp4l [896569 -> 0] len 74(74)
\x0d\x12\x00\x4a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x48\x57\xdd\xff\xfe\x07\x93\x21\x00\x00\x00\x00\x04\x7f\x00\x00\x00\x00\x00\x00\x00\x00\xe9\x5d\x00\x00\x02\x00\x00\x01\x00\x16\x20\x00\x01\x00\x00\x01\x80\xf8\xfe\xff\xff\x80\x48\x57\xdd\xff\xfe\x07\x93\x21\x00\x00
^C
2 packets captured
```

Also, if one is being curious - now it supports prefix-based socket path matching, and specifying '*' as a socket path
allows to dump **all** the communications happening over Unix sockets on the system.
Spoiler alert: *systemd* does a lot of stuff there.

## Use-case

All and all, I find the ability to dump communication happening over Unix Domain sockets to be very useful.

First, it's extremely valuable to record the interactions that happen over Unix sockets to be able to implement
intricate details of the (often undocumented) protocols.

For example, protocol used for *chronyd <-> chronyc* communication is completely undocumented, so in order to [implement
it in Go](https://github.com/facebookincubator/ntp/tree/main/protocol/chrony) I had exactly two options - reading the C source code and looking at the live traffic.

Without the ability to see what's going on over the socket,
it would have been very hard to implement parts of the protocol that are not allowed to be used over the network.

And second, once code works, it's easy to collect data for extensive unittests with a tool like `sockdump.py`.
You just fire up the script, perform various actions with commands that communicate over the socket,
and use collected dumps as fixtures/data for table-driven tests.

So while this is not something that most of the IT folks will use every day, for me it's a very useful tool in my toolbox,
and I use it fairly regularly.

And if you are interested to learn more about BPF that powers `sockdump.py` and `bpftrace`, I can highly recommend the wonderful
[**BPF Performance Tools**](https://www.brendangregg.com/bpf-performance-tools-book.html) book by Brendan Gregg.
