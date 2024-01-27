---
title: "Python is not good for production"
date: 2021-03-13
slug: python-rewrite
Categories: [IT]
tags: [Python, Golang]
---

Here, I said it.

Recently I read an excellent (opinionated) [post by rachelbythebay](http://rachelbythebay.com/w/2021/02/22/lang/) describing
things she cannot stand in programming language, and it resonated deeply with me and finally pushed me to write this.

I feel quite strongly about using Python in production, and below I'll summarize my experience and opinion.

Everyone is entitled to their own opinion, this is mine.

I'm not trying to offend anyone, so if you love Python - maybe try to see my side of things.

**TL;DR any effort to keep Python service alive or up to date with new stuff (Python 3, Type Annotations, Asyncio) is comparable to a complete rewrite, only with diminishing returns.**


## My Python experience in a nutshell

I landed **few hundred KLOCs** in Python, which included:
* writing tools and services from scratch in Python3 with and without type annotations
* migrating some medium sized services from Python2 to Python3
* adding type annotations to existing codebase
* migrating existing code to Asyncio

Here is what I think about this experience:

### Whole Py2->Py3 thing was a total mess

There are many posts about it, I'll just give one example:
It took us quite significant effort to migrate pretty good quality code (~60kloc) with decent unittest coverage,
and we still stumbled on some bugs in prod for many weeks after the migration.

And boy this breaking Py2->Py3 transition was so unnecessary!
Making `print` a function and adding new type for strings was so not worth it... from my point of view it clearly didn't justify breaking the compatibility.

### Type Annotations are good, but not good enough

I already [expressed my admiration for Python 3.5+ type annotations](/it/python-typing/).
However, after using them extensively in real life, I can point to few real problems with them:
* First, existing dynamically typed code doesn't always map nicely to ~static type annotations. Which means that you either refactor the code or use `Any` type.
* Second, they are ignored by interpreter, by design. So you end up using external type checkers like [mypy](http://mypy-lang.org/) or [Pyre](https://pyre-check.org/), and this brings multiple problems:
    - Slow-ish analysis speed, especially compared to fast modern compiled languages like Go
    - Incomplete analysis - quite often you express all types correctly, but analyzer fails to understand it
    - Type Annotations cannot improve performance, unlike [Cython](https://cython.org/)
    - Type Annotations are completely optional, and often are added as an afterthought, so not necessary influence the architecture of the program as good typing system should


### Switching to Asyncio is a big undertaking

In theory, new async Python3 sound pretty good, and if your service lives in vacuum it is quite nice.
Unfortunately, when trying to use Asyncio with existing codebase you quickly realize that to really benefit from it,
**all your dependencies need to be async**. And if for some common OpenSource libs out there already might be some Asyncio alternative,
decent chunk of your internal deps will have to be written once again.

Also it's still pretty new, so more bugs, and last time I checked reasoning about performance was really hard.


### Performance is not good at all

It's 2021 but [GIL](https://wiki.python.org/moin/GlobalInterpreterLock) is still a thing, and believe you me any CPU-bound task should never be written in Python.

Surely one can optimize hot paths of your code with [Cython](https://cython.org/) that will generate C++ code for you
(we did it with good results), or just rewrite them in different language, but if you start rewriting parts of the code, why stop?

I witnessed (and performed myself) many rewrites from Python to Go/C#/Rust/C++, even [blogged about some](/it/go-carbon/)
and every time even un-optimized POC in compiled language was performing many times faster than
optimized Python version of same service/tool.

### Startup time is horrendous

Even you write CLIs in Python (and it's quite pleasant with [Click](https://click.palletsprojects.com/), you should be aware of startup time penalty for interpreted languages.
With Python it can be really bad, and the more dependencies your code has the worse it gets.

And when you use CLI tools often, slow startup really is a death by a thousand cuts.

Thanks to widespread bad practices of say initializing Singleton client classes on init time, it gets ridiculously bad, with simplest tools taking seconds to just show '--help'.

I myself rewrote a simple CLI tool from Python to Go, bringing runtime from **28s** to **<1ms**.
All the tool did was exchanging like 6 UDP packets with local demon to gather monitoring metrics.


## Conclusion

Again, this is just my opinion, but after years of writing Python and years of writing Go, there is the conclusion I landed upon.

### Dynamic typing and interpreted nature of Python make it poor fit for production services

There have been thousands of articles on the subject, but after 11 years of working in the industry
I strongly believe that dynamic typing is not suited for services that need stability.
And yes, I know about Erlang, and yes, I'm confident it would be much better with static typing.

Sure, dynamic typing often enables faster prototyping, but if you don't throw the prototype away immediately it will cost you dearly.

I saw my fair share of huge codebases in Python, with and without Type Annotations, and in every case the problems were similar.

No amount of unittests (and don't even get me started on default testing module in Python)
and no smart IDE saves you during refactoring, every time it's like walking on a minefield.

Adding features without refactoring will increase technical debt, and refactoring will lead to runtime errors.

Decent compiler and static typing save from all of this.

### Using a better suited language will pay off

Don't be a victim of [sunk cost fallacy](https://en.wikipedia.org/wiki/Sunk_cost#Fallacy_effect), stop wasting time and effort
on Python just to get diminishing returns in the end.

From my personal experience, rewriting from Python to *any decent statically typed compiled language* is mostly trivial and always brings great results. I myself saw it being done with C++, C#, Rust, and of course Go. Worked a charm *every time*.

**If you have a production service in Python, do yourself a favour and rewrite it in a sensible language.**
