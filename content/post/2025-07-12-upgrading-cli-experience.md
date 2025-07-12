---
title: "Upgrading the CLI experience"
date: 2025-07-12
slug: upgrading-cli-experience
Categories: [IT, Personal]
tags: [zsh, fzf, bat, eza, ripgrep, fd]
---

I spend *a lot of time* in the terminal.

I practically live in the terminal at work, that's kind of a given.

But even this very post is written in [Helix](https://helix-editor.com/), running in [Wezterm](https://wezterm.org/).

And it's been like this (and even more so in my SysAdmin days) for close to 20 years.

I already wrote about [refreshing my CLI setup](/post/2024/09/22/refreshing-cli-setup/),
and how I [moved from tmux to Zellij](/post/2025/03/22/tmux-zellij/) to improve my CLI experience.

It's now time to talk about small tools that make a big difference.

A full disclaimer - as a true SysAdmin, I thought all of them to be of little value, something superficial,
something that a hipster, with a MacBook, would use while drinking pumpkin latte in a café somewhere in Palo Alto.

I'm happy to admit that I was wrong.

Anyway, let's start with the basics!

## [bat](https://github.com/sharkdp/bat)
I never thought I needed a better version of `cat` until I tried it.
Makes a huge difference thanks to the line numbers, syntax highlighting, and pagination.

Even more useful to use for file previews, for example in conjunction with `fzf` (more about it later).

I aliased `cat` to `bat` long time ago, never regretted this decision.

Although I still often pipe things to `less` out of habit, I realize that have I tried *bat* earlier in my life I'd probably just `cat` everything now.

## [eza](https://github.com/eza-community/eza)
`eza` is a modern `ls` and `tree` alternative with colours and icons.

Just as with `bat`, I aliased `ls` and `tree` to `eza` and never looked back.

Colourful, legible `ls` output makes my life in the terminal much more pleasant.
And given the fact that I never got used to the actual CLI file managers, I still rely on `ls` very often.

## [ripgrep](https://github.com/BurntSushi/ripgrep)
This one is has nothing to do with the nice colourful output.

`rg` is a much faster modern `grep`, with saner flags as a bonus. I think it's an absolute no-brainer to switch to it.

Really, I can't believe I did not give it a try years ago.

I search inside big files (we are talking multiple gigabytes big) very often at work, so it hurts to think just how much time I wasted waiting for `grep` to finish!

You'd think it is a small thing - sure, finding stuff takes one or two seconds instead of 30 - not a big deal.
But in fact because it is so fast, it doesn't interrupt the flow (you don't need to context switch or zone out while waiting for the results),
so it makes a massive impact on the overall productivity.


## [fd](https://github.com/sharkdp/fd)
`fd` is a better version of `find`.

Granted, I don't use it too often (neither did I use `find` often),
but it's frequently used by other tools and even editor plugins for picking files,
so doesn't hurt having it installed.

And unlike `find`, flag names make sense.

## [fzf](https://github.com/junegunn/fzf)
This tool alone deserves a dedicated post, and luckily there are plenty written about already.

It's unbelievable how much can be built with it to enhance the CLI experience.

I use it for several things:
* fuzzy file selection with `zsh`, with the excelled `**`+`Tab` shortcut. Absolute must for anyone using `zsh`.
* fuzzy history search with `zsh`.
* custom file picker with content preview.
  At work, we have a tool to search the big monorepo content, think `grep` but distributed and over a very large repo.
  With `fzf` + `bat` I can use it while having a nice syntax-highlighted preview of the file, down to the exact position inside the file.
  Massive improvement to my workflow.

I'm still learning this amazing tool, but the examples you can find on the internet are absolutely mad.

## Conclusion

Discovering tools like these is precious to me, and the improvements they made in my experience is what
drives me to continue the experimentation and search for better tools.

That's how I discovered and eventually [migrated to Zellij](/post/2025/03/22/tmux-zellij/).

That's why I wrote this post in `helix` and not `vim`.

I think it's paramount to keep experimenting, trying new tools, even if your setup already seems fine.

I also admit that it can be very hard to find the energy or mental capacity to do it,
especially when facing time and performance pressure at work.

Sometimes it may take months or even years for me to dedicate a bit of resources for the experimentation,
but every time I do it I'm rewarded with some meaningful discovery, and it keeps me motivated to *try* and find the time to continue doing this.
