---
title: "Taking Notes"
date: 2021-05-23
slug: taking-notes
Categories: [Personal]
tags: [Evernote, QOwnNotes, Joplin]
---

In the *days of yore* it was common for people to keep a diary.
I myself was always a fan of this idea, but could never actually get started with it.

My handwriting is absolutely terrible, to the point that I can't decipher my own notes,
which rules out writing diary in an old-fashioned way.
And all diary-like mobile apps seem to add too much friction.

I kinda solved this for my needs few years ago by writing an simple app that allows me to quickly collect each day stats and activities in under 1 minute,
but that's not the topic of this post, I'll write about it someday later.

Anyway, instead of keeping a diary I started to write notes about stuff I'm interested in.

## A bit of history

Since 2012 I have notes with mini-reviews and ratings of:
* books I read
* music albums I bought
* video games I played

And of course I kept notes with random thoughts, ideas and stuff.

I always used my phone (Android back then, iPhone now) to take those notes, and when I started doing it the only good software available was **Evernote**.

It was actually pretty good back then, and one of the first things I tested was **export** functionality, which worked very well.

I used Evernote from 2012 to ~2014 when I started playing with [personal VPS](/it/Личный-vps/) and the idea of fully self-hosted environment.
With personal VPS I switched to Tomboy and Tomdroid with Owncloud sync, which worked ok-ish. I exported all notes from Evernote to Tomboy without any issues, and kept using this setup for over 1.5 years.

When I was [done playing with VPS](/it/goodby-vps/) in 2015, I migrated back to Evernote, and used it till 2021.

Unfortunately over the years Evernote slowly turned into utter garbage,
and with latest obnoxious 'redesign' I was finally done with it.

And of course first thing I discovered is that they seem to have killed 'export' in any shape or form!
At least it's not present in the mobile app or website.

There still is an option to export notes using their API, but with the trajectory Evernote took I'm sure it will be deprecated/hindered somehow pretty soon, just to keep the users locked in.

Anyway, I exported all my notes and started to look for the replacement.

But before I share my findings, I need to explain how I use note-taking apps.

## How I use personal notes

My personal notes usage pattern was pretty much the same since 2012, I update relevant entries once
I form an opinion about a book/album/game, or whenever I had an idea to write down.

I always to it from my phone, because it's always with me.

All I ever needed is basic formatting support (I always wished Evernote just let me use Markdown instead of their ever-changing WYSIWYG editor), nothing else.

In my head, I imagined perfect personal notes-taking setup as this:
* Desktop app with Markdown support and import/export options
* Simple mobile app to add/edit notes
* Synchronization via Dropbox, i.e. notes are just `*.md` files in a dedicated directory.
* Opensource

## How I write work-related notes

A colleague of mine introduced me to an app called [**Notational Velocity**](https://brettterpstra.com/projects/nvalt/), which implements really cool note-taking concept:
you only have an editor and a search field, where you can either find a note by it's content or name, or create a new one.
No save button, no nothing - you type stuff in, it's immediately saved and instantly searchable.

This approach works brilliantly and helps me with all work stuff ever since.

But because Notational Velocity is MacOS-only, and I left this platform years ago, I had to find an multi-platform alternative.

I found it in a form of opensource [**QOwnNotes**](https://www.qownnotes.org/) app, which works really well on desktop and
stores my notes simply as named markdown files in my work Dropbox folder.

I use it exclusively for work stuff, so lack of mobile app support was never a problem.

For personal notes though I need something with similar approach **and** mobile app.

## Best Evernote replacement I found

And you know what? Such setup finally exists thanks to awesome [**Joplin** app](https://joplinapp.org/).

I couldn't be happier with it, it does exactly what I always wanted my notes-taking app to do.

Opensource, no cruft, no terrible WYSIWYG editor, syncing via Dropbox/Nextcloud. Simple and lightweight on the phone, works well on PC.

I can wholeheartedly recommend it, and it seems like it's doing quite well in terms of development, with second [Google Summer of Code participation](https://joplinapp.org/gsoc2021/index/) and active github repo.

I just wish I made this wonderful discovery sooner!

## Sidenote

While exporting everything from Evernote I was amused that I have notes from that long ago, and it's pretty cool
to read what games I liked in say 2013 and why.

I can definitely recommend taking notes just for yourself, it will bring you lots of fun in years to come.
