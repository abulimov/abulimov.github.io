---
title: "Fun experiments with Go memory usage"
date: 2024-01-27
slug: golang-memory
Categories: [IT]
tags: [Golang, Programming]
---

While working on a big Go program that processes data I began to wonder if our memory usage is adequate for the amount of data we deal with.

My starting point was this question - *If the output of this service is a text file that is only few Gigabytes in size,
why does it take significantly more memory to produce this file?*

This lead to a series of experiments which I hope will be interesting for anyone caring about writing efficient code.

## Initial dataset and goal
Here is our test dataset (copied from service's output):

```
wc -l ~/tmp/data-1696012970
30084004 /home/abulimov/tmp/data-1696012970

ls -lh ~/tmp/data-1696012970
-rw-r--r-- 1 abulimov abulimov 936M Oct 2 14:32 /home/abulimov/tmp/data-1696012970
```

Which gives us **30M records in almost 1Gb**, ~31 bytes per line.

All lines are pure ASCII.

The task we are experimenting with is based on the actual workload our service does.

**Let's simply read those 30M lines into memory, each line stored separately, and see how much memory it will actually take.**

## Reference C program

Here is the most basic C program that does that, which will serve for us as a reference point:

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[])
{
    char const* const fileName = argv[1];
    FILE* file = fopen(fileName, "r");
    size_t len = 0;
    ssize_t read;
    char *line = NULL;
    char *realLine = NULL;
    size_t charCount = 0;
    size_t arraySize = 1;
    char **lines = malloc(arraySize * sizeof(char *));

    while ((read = getline(&line, &len, file)) != -1) {
        realLine = malloc(sizeof(char) * read);
        strncpy(realLine, line, read);
        lines[charCount] = realLine;
        charCount++;
        if (charCount >= arraySize) {
            arraySize = 2 * arraySize;
            char** myarray = realloc(lines, arraySize * sizeof(char *));
            if (myarray) {
                lines = myarray;
            } else {
                return 13;
            }
        }
    }
    printf("lines: %ld\n", charCount);
    fclose(file);
    return 0;
}
```

building it with `gcc -O2 -Wall main.c` and running with `time` gives us this result on my M1 MBP
(here and later on I edited the time output to remove information that is not interesting to us):

```
/usr/bin/time -l ./a.out ./data-1696014531
lines: 30085159
        1.90 real         1.59 user         0.28 sys
          1410913216  peak memory footprint
```

**So to store 30M C strings, each around 31 bytes long, we would need roughly 1.4Gb of memory.**

Or around 47 bytes per line. Which makes sense when we think about what it takes to store data in memory - on a 64bit system we need at least 8 bytes for pointer + 8 bytes for each heap-allocated array size.

*These last 8 bytes can be a surprise (we won't see it in the code after all), but they make total sense when you think of it. Of course when we
allocate memory, under the hood somewhere the size of this allocation must be tracked. Otherwise, how would the computer know what to do when you call
free() without providing the size that needs to be freed?*

Summing it up, we get exactly 47 (31 + 16) bytes per line, so now we know the baseline values.


## Naive Go code

Let's look at the Go code to do the same:

```
package main
import (
  "os"
  "io"
  "bufio"
  "fmt"
  "runtime"
  "log"
  "time"
)

func printMem() {
  var m runtime.MemStats
  runtime.GC()
  runtime.ReadMemStats(&m)
  fmt.Printf("Alloc = %v MiB", m.Alloc/1024/1024)
  fmt.Printf("\tTotalAlloc = %v MiB", m.TotalAlloc/1024/1024)
  fmt.Printf("\tSys = %v MiB", m.Sys/1024/1024)
  fmt.Printf("\tNumGC = %v\n", m.NumGC)
}

func main() {
  f, err := os.Open(os.Args[1])
  if err != nil {
    log.Println(err)
    os.Exit(1)
  }
  start := time.Now()
  l := make([]string, 0)
  scanner := bufio.NewScanner(f)
  for scanner.Scan() {
    line := scanner.Text()
    l = append(l, line)
  }
  printMem()
  log.Printf("done with %d lines in %v", len(l), time.Since(start))
}
```

Running it provides us with somewhat disappointing results:

```
/usr/bin/time -l ./main_simple ./data-1696014531
Alloc = 0 MiB	TotalAlloc = 3454 MiB	Sys = 2260 MiB	NumGC = 17
2023/10/23 15:05:59 done with 30085159 lines in 1.912067292s
        1.96 real         2.45 user         0.51 sys
          2357941696  peak memory footprint
```
  
Hm, **2.3Gb for the same task**, that's quite an overhead! Let us see why does this happen?

## String data type difference, and mysterious overhead

First, let's compare how we deal with strings.

In C, we have infamous `\0`-terminated byte sequences, no overhead and no safety.

In Go, we have this type under the hood:

```
type string struct {
    data uintptr
    len int
}
```
  
As you can see, it is much safer as we have `len` stored next to the byte sequence.

However, this gives us extra 8 bytes per string, which when multiplied by 30M is a significant 230Mb increase in memory usage.
Which is actually fine, because as you've seen when we allocate things on the heap, we lose same 8 bytes implicitly anyway, just without any real safety guarantees.

What is very interesting is that Go is clever enough to store structs in slices in contiguous memory, so simply putting things into slices doesn't have overhead of storing heap pointers.
This example shows that you can happily allocate billions of empty structs in Go without OOMing:

```
package main

import "math"

func main() {
    a := make([]struct{}, math.MaxInt64)
    println(len(a))
}  
```

This is why it is recommended to use `map[string]struct{}{}` instead of `map[string]bool{}` when implementing sets.

Going back to the task at hand - despite Go's smart tricks around contiguous memory,
my experiments show that whenever reading data into strings using standard library always leads to pointers escaping to the heap.

Combining all this theorizing brings us to the anticipated memory usage of around 1.6Gb. Where did we lose the rest?

I was quite puzzled with this question, and it took me some time to figure it out.

## Should we use `[]byte`

While thinking about that lost memory, I experimented with different data structures. Surely when we use raw `[]byte` we should see better memory usage?

Wrong!

In Go, `[]byte` is actually bigger than `string`:

```
type slice struct {
    data uintptr
    len int
    cap int
}
```
  
We store extra 8 bytes of current capacity per `[]byte` instance!
Which means that against our intuition, using raw bytes is less effective than strings. If you need experimental proof - please check out Appendix A.

## Blame the GC?

Maybe we should blame the *Garbage Collector*? Let's turn it off and see!

```
GOGC=off /usr/bin/time -l ./main_simple ./data-1696014531
Alloc = 0 MiB	TotalAlloc = 3454 MiB	Sys = 3556 MiB	NumGC = 1
2023/10/23 15:25:07 done with 30085159 lines in 2.486294584s
        2.68 real         0.97 user         1.14 sys
          3701334016  peak memory footprint
```

Ouch, now we consume 3.6 Gb. What is going on here? What was it that we didn't collect?

I have a suspicion, but let's check one more assumption around GC - maybe it's just lazy?

Let's use `GOMEMLIMIT` environment variable and set it to our anticipated 1.7Gb to make GC sweat:

```
GOMEMLIMIT=1700000000 /usr/bin/time -l ./main_simple ./data-1696014531
Alloc = 0 MiB	TotalAlloc = 3454 MiB	Sys = 2259 MiB	NumGC = 22
2023/10/23 15:39:48 done with 30085159 lines in 2.37959025s
        2.44 real         3.94 user         0.74 sys
          1888245120  peak memory footprint
```
  
Well, it did sweat (before the `GOMEMLIMIT` we had `NumGC=17`, now it is `22`), but the result didn't change much...
Also, `time` seem to have missed the brief moment when we consumed 2.2Gb, oh well. Something else must be at play.

## Answer to the lost memory question

I wrote a lot of Go code in my life, so quite quickly I had a suspicion about the 'lost' memory. Let's see if it is correct.

Let's pre-allocate the `[]string` slice to avoid growing it and copying the data over and over again to the new memory region, and change one line:

```
l := make([]string, 0, 31*1000000)
```

and then compile and run our tiny binary:

```
/usr/bin/time -l ./main_simple ./data-1696014531
Alloc = 0 MiB	TotalAlloc = 1518 MiB	Sys = 1590 MiB	NumGC = 3
2023/10/23 15:46:03 done with 30085159 lines in 1.080537584s
        1.10 real         1.02 user         0.42 sys
          1662112000  peak memory footprint
```

Yay, now the math makes sense! **We use 1.6Gb**, just as we expected. Also notice the run time and number of GC.
We now execute twice as fast, and only ran GC 3 times. Finally, the numbers make sense.

## Conclusion

The mystery is solved, and we have a solid piece of advice to anyone writing efficient Go code - **always pre-allocate your slices**.

Luckily, [`golangci-lint`](https://golangci-lint.run/) runs `prealloc` linter that warns you about missed pre-allocation opportunities.

Also, now we know that to simply do anything with 30M of relatively short strings in memory,
one would need around 2x the space they take on disk, and thus our service in question is vindicated - it uses reasonable amount of memory for the task at hand.

### Appendix A: Memory arenas

As we have already gone quite deep in the whole Go memory/GC thing, let's talk about **ways to avoid GC overhead**.
Using *CGO* surely would be one of them, but recently another one was added.

Enter the **Arena**! Or to be more specific, [experimental Go 1.20 feature called 'memory arenas'.](https://uptrace.dev/blog/golang-memory-arena.html)

As of now, arenas do not support storing strings in them, so let's rewrite our program to use bytes and measure the memory (with pre-allocated slice).

We get `Sys = 1830 MiB`, so just as predicted around 200Mb overhead over strings.

Now what if we use arenas? The whole premise is that you have a whole region of memory that is not touched by GC, and is allocated/deallocated at once.
Which in our case means we should save around 200Mb on pointers, right? Let's see if this stands true.

```
package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
    "runtime"
    "time"

    "arena"
)

func printMem() {
    var m runtime.MemStats
    runtime.GC()
    runtime.ReadMemStats(&m)
    fmt.Printf("Alloc = %v MiB", m.Alloc/1024/1024)
    fmt.Printf("\tTotalAlloc = %v MiB", m.TotalAlloc/1024/1024)
    fmt.Printf("\tSys = %v MiB", m.Sys/1024/1024)
    fmt.Printf("\tNumGC = %v\n", m.NumGC)
}

func appendA[T any](data []T, v T, a *arena.Arena) []T {
    if len(data) >= cap(data) {
        c := 2 * len(data)
        if c == 0 {
            c = 1
        }
        newData := arena.MakeSlice[T](a, len(data)+1, c)
        copy(newData, data)
        data = newData
        data[len(data)-1] = v
    } else {
        data = append(data, v)
    }
    return data
}

func main() {
    f, err := os.Open(os.Args[1])
    if err != nil {
        log.Println(err)
        os.Exit(1)
    }
    start := time.Now()
    mem := arena.NewArena()
    defer mem.Free()
    l := arena.MakeSlice[[]byte](mem, 0, 31*1000000)
    scanner := bufio.NewScanner(f)
    for scanner.Scan() {
        line := scanner.Bytes()
        lline := arena.MakeSlice[byte](mem, len(line), len(line))
        copy(lline, line)
        l = appendA(l, lline, mem)
    }
    printMem()
    log.Printf("done with %d lines in %v", len(l), time.Since(start))
}
```
  
And just as we expected, using arenas takes same amount memory and run time is somewhat faster:

```
/usr/bin/time -l ./main_arena ./data-1696014531
Alloc = 912 MiB	TotalAlloc = 1621 MiB	Sys = 1661 MiB	NumGC = 4
2023/10/23 16:08:08 done with 30085159 lines in 985.003042ms
        1.02 real         0.97 user         0.46 sys
          1733939584  peak memory footprint
```
  
Sadly it is likely that [this feature will never be part of the language](https://github.com/golang/go/issues/51317),
but that doesn't prevent us from playing with it, having fun and learning more about Go and GC.

### Appendix B: Test environment

All tests were conducted with Go 1.21.
Initial set of experiments was done on Linux running on Intel CPU (where for example the arena speed-up was more prominent),
and the final numbers for this note were collected on M1 MBP (macOS and ARM64).
