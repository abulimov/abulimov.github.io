---
title: "More nice things for this blog"
date: 2026-10-26
slug: blog-nice-things
Categories: [Personal]
tags: [Blog, Hugo]
---

I continue to improve this website to make it a [better representation of me on the Internet](/post/2025/09/18/added-lists/).

In the past year and a half, I have:
* [added dark mode support](/post/2025/05/11/blog-dark-mode/). I myself use dark mode exclusively at work, so it was long overdue.
* [revamped the reviews](/post/2025/09/07/better-reviews-and-retrospective/). This section grew unwieldy over time, and needed a better structure.
* [added a 'lists' section](/post/2025/09/18/added-lists/). More things about me, with nice Mermaid timelines.
* [added a 'DIY' section](/post/2025/11/08/added-diy/). A simple gallery of things I've built over the years.
* [added site-wide search](/post/2026/10/24/added-search/). Easy way to search this website without ripgrep.

This time I added a few more things (all made easy thanks to [Hugo](https://gohugo.io)).

## Estimated reading time

Super simple: Hugo has a `ReadingTime` [method for this](https://gohugo.io/methods/page/readingtime/), and now this info is added to the post header.

## Table of Contents

Again, super simple, `TableOfContents` [method exists](https://gohugo.io/methods/page/tableofcontents/) and renders a nice nested list.
I wrapped it in a [`<details>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details), sweet.

## Syntax Highlighting

I still can't believe that my blog has lacked it since I moved to this minimalistic theme.

Once again, [Hugo has everything built-in](https://gohugo.io/content-management/syntax-highlighting/).
Even with my default setup, the only thing missing was adding language fences to the code blocks.

For my use case, the only complication was supporting the dark mode.

Thankfully Hugo can generate syntax highlighting CSS that I simply conditionally include in the `@media (prefers-color-scheme: dark)` block.

I used 'catppuccin-latte' and 'catppuccin-mocha' for the light and dark schemes respectively,
same ones that I use myself for coding.

A good example of a post that has a significant amount of code to highlight is my
[exploration of memory usage in Go](/post/2024/01/27/golang-memory/), and it looks just lovely now.

## Anything else?

I don't have any other improvement ideas for now, but that's fine.

As I read other people's blogs, I sometimes notice nice things that I consider worth adding to my website.

And sometimes I just learn about new technology at work, and use it here, like Mermaid diagrams.

I add those improvement ideas to a dedicated [Trilium note](/post/2026/08/23/joplin-to-trilium/) in a kind of a backlog,
and implement them whenever I have the time and energy.

Like today, with this list of improvements.


