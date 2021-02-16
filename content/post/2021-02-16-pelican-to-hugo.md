---
title: "Moving from Pelican to Hugo for this blog"
date: 2021-02-16
slug: pelical-to-hugo
Categories: [Personal]
tags: [Golang, Hugo, Pelican]
---

Since I no longer enjoy working with Python in any shape or form, it was only a matter of time (mostly a matter of *my free time*)
for this to happen. I've migrated this blog from Pelican static site generator (written in Python) to Hugo (written in Go).

It by no means reflects on Pelican as a piece of software (it's actually pretty good). 
It's more about my disdain for Python, and awesome experience I had with Hugo and Go language in general.

One of the reasons this blog was inactive is the fact that setting things up was always too much work in case of Pelican.
Maintaining `$PYTHONPATH`, dealing with `pip3` and stuff - meh...

Blogging should be effortless and fun, but unfortunately for me using Pelican just triggered PTSD.

With Hugo all I need is a single statically built binary that does everything - pretty neat.

Another goal I had for this migration was to make this blog as lightweight and minimalistic as possible.
Very simple theme, no more Disqus, Google Analytics, JavaScript or any other heavyweight stuff.

This whole page is just few kilobytes, and I plan to keep it as lean as possible. Full load of something like 'medium.com' takes 10+ seconds with a good broadband, I don't think it's anywhere near acceptable for a predominantly text content.

As much as I admire ReactJS and modern single page webapps, I don't think most of the pages on the Internet should go heavy on it,
and definitely not simple blogs.
