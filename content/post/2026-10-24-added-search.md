---
title: "Added search"
date: 2026-10-24
slug: added-search
Categories: [Personal]
tags: [Blog, Hugo, Pagefind]
---

After 13 years of blogging, this blog grew relatively big.

At least big enough that I myself can't always remember what I wrote about, and where.

The solution is of course obvious - just add a search feature!

However, this is a statically generated website.

All the pages are converted from Markdown to HTML by [Hugo](https://gohugo.io) and pushed to Github Pages.

Which means there is no backend that normally runs the search for us.

Thankfully, there are client-side search libraries, and some quick research
led me to [Pagefind](https://pagefind.app/).

It is a client-side JS library plus a Rust CLI to build the index for any website.

The [documentation](https://pagefind.app/docs/) is superb, and it took me only a couple of minutes to add
the search page to this blog.

The only question was how to incorporate this new functionality into the existing blog.

Currently, my philosophy for this website is to keep it as lightweight and minimalistic
as possible.

Hence, there is no JavaScript loaded anywhere except on a few pages that use Mermaid diagrams.

And the main CSS is 58 lines.

So instead of adding a JS lib to every page, **I limited the damage to a single
[/search](/search/) page**.

This way, when you are reading this post, it remains pure HTML
plus a tiny bit of styling. But on a dedicated page there is now an interactive site-wide search thanks to Pagefind.

Pretty neat if you ask me!
