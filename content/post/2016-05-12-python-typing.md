---
Title: Python Type Hints are awesome
Date: 2016-05-12
Tags: [Python, Programming]
Slug: python-typing
Url: it/python-typing
Categories: [IT]
---

I really love [Julia Evans's blog](http://jvns.ca), she writes with such excitement
and enthusiasm about every new bit of technology she learns. For me, this is what
makes our job so great - we can learn something new and cool almost every day.

And recently I've felt very excited with some of new abilities Python
now have. I'm talking about including of [PEP 484](https://www.python.org/dev/peps/pep-0484/),
which describes Type Hints, in Python 3.5 (old news, I know).

I'm a big fan of [static analysis](https://en.wikipedia.org/wiki/Static_program_analysis)
(I love when computer helps me to spot mistakes and bugs, and have even written
a [Linter for HAProxy configs](https://github.com/abulimov/haproxy-lint)),
so when I've found that Python 3.5 has gained standard ability to specify
types for function parameters, return values and local variables, I was eager to test it.

Just to show what I'm talking about, here are some basic example of Type Hints:

    :::python
    # without Type Hints
    def greeting(name):
        return 'Hello, {}'.format(name)
    # with Type Hints
    def greeting(name: str) -> str:
        return 'Hello, {}'.format(name)


and with generics:

    :::python
    from typing import List

    def greeting(names: List[str]) -> str:
        return 'Hello, {}'.format(', '.join(names))

Fortunately, [PyCharm IDE](https://www.jetbrains.com/pycharm/) already has full
support of PEP 484, so I've immediately started adding Type Hints to
[my pet project "lyricstagger"](https://github.com/abulimov/lyricstagger).

After some experiments and adding types to actual code I can safely conclude that
Type Hints are awesome:
they let us express all the information (in a standard way, yay!) about function
parameters and variable types that we already hold in our mind,
so that IDE or linters can help us by checking that we are passing correct
values to our functions. Using Type Hints feels much more natural to me than
using one of several ways of specifying type information in docstrings.

I was writing a lot of code in [Go](http://golang.org) programming language
last year, and got used to all the benefits of static typing. Now I can
be more confident in my Python code, because static analysis with Type Hints
can catch many common mistakes even before I run any tests.

And you don't need to stick with Python 3.5 to use type hinting,
the whole `typing` module was [published in pip](https://pypi.python.org/pypi/typing)
and can be easily installed and used with Python 3.2+.

If you are as excited about Type Hints in Python as I am,
you can read more about them in
[JetBrains PyCharm blog](http://blog.jetbrains.com/pycharm/2015/11/python-3-5-type-hinting-in-pycharm-5/).
