Title: Python 3.6 f-strings rant
Date: 2017-07-24
Tags: Python, Programming, Rant, Golang
Slug: python3-fstrings

Python 3.6 introduced a new way to format strings, called
[**Formatted string literals**](https://docs.python.org/3.6/reference/lexical_analysis.html#f-strings),
or just *f-strings*. Everyone on the internet
seem to be happy about it. I'm definitely not.

For starters, Python 3 already had 3 built-in ways of doing it before.
Just think about it... 3 ways to *format strings* in language that declares simplicity as a goal:

> There should be one-- and preferably only one --obvious way to do it.
> - [The Zen of Python](https://www.python.org/doc/humor/#the-zen-of-python)

These methods are:

* Using `%` (modulo) operator (old way, supported in logging module)
* Using `.format()` string method (relatively new way)
* Using [*template strings*](https://docs.python.org/3/library/string.html#template-strings) (very old and quite slow way)

And I'm not even talking about basic string concatenation.

And as this is clearly not enough for *simplicity*, they've just added
another method. It works almost like `.format()`:

```python3
>>> foo = "bar"
>>> f"f-strings allows me to use {foo.upper()} just like this"
"f-strings allows me to use BAR just like this"
```

The idea is to directly use names from current scope for formatting.

So now we have 4 ways to format strings, all of which can be mixed up.
I'm already sick of seeing all kind of mistakes like using `{}` with
modulo formatting, or `%s` with `.format()` formatting, mixing both methods
in the same file. And as programmers do mostly **read** the code, I do care
about it's comprehensiveness and readability.

Another concern is tooling support. Python is already looking bad
from this point of view, having just [pylint](https://www.pylint.org/)
as a standalone linter (sorry, but *pyflakes* is a joke compared to it).
[PyCharm](https://www.jetbrains.com/pycharm/) is brilliant without any doubts,
but it's not everyone cup of tea. And while even *pyflakes* can handle
checking for usage of uninitialized variable, doing the same with f-strings
is more complicated, and is not supported for now AFAIK.

Returning to Python from Go land, all of this really bothers me.
While Go devs are thinking about [Simplicity Debt](https://dave.cheney.net/2017/06/15/simplicity-debt),
Python folks just keep adding features.

And while I'm quite [happy with Python 3 Type Hints](/it/python-typing/),
because it actually helps to understand the code by clearly indicating
argument types, I'm absolutely not happy with f-strings, especially seeing how
they are already breaking linters and cutting off Python 2 compatibility at work.
