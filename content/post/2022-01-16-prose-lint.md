---
title: "Code-like linting for prose"
date: 2022-01-16
slug: prose-lint
Categories: [Personal, IT]
tags: [Vale, Blog]
---

I'm a big fan of static analysis and linting for code.

If a computer can do it automatically - why rely on humans to do the same thing?

That's one of the reasons why I'm such a big proponent of static typing.

I try to bring linting everywhere: 
* When I had to deal with huge and complex
HAProxy configs  - I [wrote a linter](https://github.com/abulimov/HAProxy-lint) myself.
* When later at different place I had to deal with complicated business logic expressed
as a state machine - I used Python AST to write a linter for it, and analyze cycles, dead ends and complexity.

And of course I use existing open-source linters whenever possible.

Anyway, I was intrigued when I read about [`Vale`](https://github.com/errata-ai/vale)
in recent issue of excellent [Golang Weekly newsletter](https://golangweekly.com/issues/394).

The idea of bringing code-like linting to prose definitely sounds very appealing,
and the tool being syntax-aware and written in Go added to the excitement.

I tried it with both of my blogs (first the [Scale Models](https://models.bulimov.ru/), then this)
and with some configuration tweaking it's just what I need!

It works just as it should - tons of independent lint rules, with flexible configuration.
And the fact that it is syntax aware is great - no weird issues just because I'm using Markdown.

Static text-based config and rule sets are designed to be a [part of the repo](https://github.com/abulimov/abulimov.github.io),
which makes it so natural to enable advanced auto checks that don't depend on the environment.
I totally see why `Vale` is already used by so many big projects to lint documentation,
and I didn't even start to write custom rules.

You may wonder why I was happy to see it written in Go? Because it promises *speed*!
I'd be equally happy to see Rust or C/C++ there. And that's because I had already experimented with
Python-based [`proselint`](https://github.com/amperser/proselint/) some time ago, and it's just so slow...

Just some numbers to contemplate: running `proselint` on all posts in this blog takes crazy **50 seconds.**
`Vale` has more checks (including all of the `proselint` rules), but running it on the same content takes mere **1.5 seconds**.
Why does it matter? Because I wanted it to be a part of pre-push checks, and also integrate in my text editor,
and fast tool make all the difference to one's productivity.

So far I'm really glad I started to use `Vale`, and honestly a bit embarrassed that I didn't think about
something like this before, given my long standing love for linting.


