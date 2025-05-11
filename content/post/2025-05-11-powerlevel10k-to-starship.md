---
title: "Moving from powerlevel10k to Starship for my zsh prompt"
date: 2025-05-11T16:30:00
slug: powerlevel10k-to-starship
Categories: [IT, Personal]
tags: [zsh, Starship]
---

Last year, when I wrote about [refreshing my CLI setup](/post/2024/09/22/refreshing-cli-setup/), I explained why I picked [powerlevel10k](https://github.com/romkatv/powerlevel10k) over [Starship](https://starship.rs/).

**Starship is a minimal, cross-shell prompt written in Rust.**

Well, things have changed, I re-evaluated my choice and switched to Starship.

Back in September 2024 I wrote:
>In the case of *Starship* for example, while the idea of a cross-platform, compiled prompt is interesting, paying the cost of spawning a process (or multiple) each time is just absurd to me.
>Also, saying it's "really really fast" in the readme, but providing no proofs or benchmarks - that's lame, and there is even an [issue open for this](https://github.com/starship/starship/issues/5593).

And I still think that saying 'really really fast' without any proof is silly!
But I sure changed my mind regarding the latency, plus another factor came into play.

It started with a simple thing - I wanted to customize my prompt just a bit, so that it shows the hostname *only* when it's not running in [Zellij](/post/2025/03/22/tmux-zellij/) (simply checking if `$ZELLIJ` environment variable is set).

A convenience thing really, I already had hostname as a part of tmux (and now Zellij) status bar, but wanted to see it when in the bare shell.

All because at work all my development happens on the remove server, and I often have more than one of those, so need to be able to distinguish them instantly with and without a terminal multiplexer running.

Anyway, wanting this customization made me look at powerlevel10k closely, and oh boy the code is **inscrutable**.

The author did an amazing job writing the thing, but the nature of writing anything in an obscure shell dialect is such that no matter how hard you try, it still will be horrible to read.

Sure enough, powerlevel10k did not have a way to do what I want outside of writing a custom prompt segment.
Not a big deal, I've already done it before to support showing the branch name from a special VCS we use at work.

However, reading all that zsh code made me realize how fragile and convoluted it is.
Which in combination with my love for strongly and statically typed languages made me try Starship once again, just to see if there is a simple way to achieve what I want there.

And there was, as simple as it gets:
```
[hostname]
ssh_only = false
detect_env_vars = ['!ZELLIJ']
```

Porting my custom VCS branch command was also trivial, and so was replicating my prompt visuals.

Once I was sure it works just as I want, I decided to see how bad the latency is - after all, we still have to fork-exec a new process every time!

Turns out, it's not noticeable at all.

And `starship` provides a lovely breakdown of how long each prompt segment took.

Here is what it looks like on my personal laptop running WSL2, where I write this blog:
```
❯ starship timings

 Here are the timings of modules in your prompt (>=1ms or output):
 git_status  -   8ms  -   "[?⇡] "
 directory   -  <1ms  -   "abulimov.github.io "
 git_branch  -  <1ms  -   "on / sources "
 character   -  <1ms  -   "❯ "
 fill        -  <1ms  -   " "
 line_break  -  <1ms  -   "\n"
 time        -  <1ms  -   "at 16:58:14 "
```

That's actually pretty good to me. Sure, it doesn't account for the actual spawning of the process, but modern Linux kernel ensures it's as fast as it gets.

I have to admit - sane, short and declarative config won me over.
The confidence in software written in a modern compiled language is also a nice bonus, not gonna lie.

And if I ever move away from zsh, I won't need to change a thing regarding my prompt, since Starship is shell-agnostic.
