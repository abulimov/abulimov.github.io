---
title: "Switching from Tmux to Zellij"
date: 2025-03-22
slug: tmux-zellij
Categories: [IT, Personal]
tags: [tmux, zellij]
---

When I wrote about [refreshing my CLI setup](/post/2024/09/22/refreshing-cli-setup/), I mentioned how I gave [Zellij](https://zellij.dev/) a try,
but couldn't find compelling reasons to replace tmux with it.

I also said that I will continue to experiment with it to see if I change my mind.

Well, I'm happy to report that I found a couple of very good, if not immediately obvious, reasons that compelled me to switch to Zellij as my daily driver.

# My reasons to use Zellij over tmux

## Discoverability of the features

This is the main feature that won me over.

I have been using tmux for well over a decade. Yet I always felt like learning about any of the features it has is hard.
How can one learn about using `setw synchronize-panes` to send input to all panels at once, without looking up things online or digging through the manual?

I know from the experience that when I'm focused working, I most likely will not have time to research whatever functionality may be only occasionally useful.

For example, I may know that tmux supports sending your key presses to all panes at once, but if I don't remember by heart how to do it - I won't use it in a pinch.

Zellij authors clearly understand this problem, and that's why it has this truly great status bar with all the context-related shortcuts enabled by default.

Let's see how this can be useful with a real-life example.

I was working, and running commands to debug stuff. As a result, a tool dumped a bunch of useful information on the stderr which I wanted to process and save.

Re-running the tool while re-directing the output was not an option since the state of the system already changed.

The output was big enough to cause big pain when copying screen by screen with a mouse.

Solution with Zellij: `Ctrl-s` to enter search mode (which you do anyway to look at the scroll back), look at the status bar that helpfully changes to say `e Edit scrollback in default editor`, press `e` and happily copy and edit the needed part of the output in Vim.

Solution with tmux: `Ctrl-b + ?`, read through the list of all key bindings, fail to find anything relevant.
Look up things online, read about copy mode and buffers.
Finally, enter the copy mode, select the output, yank it, and use `:save-buffer`.

Clearly, with both tools it's relatively easy to achieve the end goal. But, when doing this in a pinch, under pressure, or simply while tired - Zellij's approach has a clear advantage of being very easy to discover right in your terminal window, right when you need it.

The same applies to other less frequently used features like floating tabs.
Would I remember how to enable something like this if I need it once a month? Of course not!
But if I can *see* a `Alt-f` shortcut to enable floating tab *right on screen* - that makes all the difference.

## Layouts

Second feature that I use all the time.

Zellij provides an expressive way to [define layouts](https://zellij.dev/documentation/layouts.html).

At work, I use it to start a new session with three tabs open, one for each of the repositories I often work with, with each tab split into two horizontal panes.

At home, I use a [simpler layout](https://github.com/abulimov/dotfiles/blob/04331f1cff1a1a87a79f737e788fbdd6e75b9dd8/home/.config/zellij/layouts/default.kdl) which just puts tab bar at the bottom (that's how I'm used to having it thanks to years with tmux) and status bar at the top.

With tmux, I had a bash script sending commands to the tmux instance to achieve the same effect, but it's much easier and elegantly done with the layouts in Zellij.

It's not that I start new sessions often (I mostly `attach` to the existing one), but it saves time whenever I need to start from scratch.

# What's missing in Zellij for me

There is just one thing that I miss - automatically enabling 'scroll' mode when scrolling pane content with mouse.
The scrolling works just fine, but Zellij requires an extra `Ctrl-s` to enable search and navigation with PgUp/PgDown.

There is an [open issue](https://github.com/zellij-org/zellij/issues/605) about it, but sadly this feature is not yet implemented.

# Exciting future for Zellij

I love the fact that Zellij is under active development.
They keep adding cool stuff like the ability to pin floating tabs, or extensive Plugin API, or tips at startup.

I can't imagine doing my work without a terminal multiplexer, and it's exciting to finally see progress and competition in this space.
