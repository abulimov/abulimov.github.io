---
title: "Refreshing my CLI tools setup"
date: 2024-09-22
slug: refreshing-cli-setup
Categories: [IT, Personal]
tags: [zsh, tmux, vim, neovim, zellij]
---

Recently I decided to get out of my shell (pun intended) and check out the latest and greatest in shells, terminal multiplexers and terminal-based text editors.

After all, It's been 8 years since I took a fresh look at how I use those invaluable CLI tools.

I still remember how on one of my first jobs I got so engrossed in the work that for a first month or so I completely neglected setting up my work machine,
and worked in a stock Debian shell and terminal, which sure looked like a dog's dinner. All with default video driver, so fonts looked appropriately bad.

Nowadays, I can't afford to subject myself to such torture. My tired eyes simply won't tolerate this, and nor will my wrists thank me if my CLI setup is not ergonomic.
That's why I invest time in properly setting up my terminal environment.

## Starting setup

I began this research with the following setup:

* `zsh` + [zprezto](https://github.com/sorin-ionescu/prezto) with a custom one-line theme
* `tmux` with [*tpm*](https://github.com/tmux-plugins/tpm) and basic plugins like [*pain-control*](https://github.com/tmux-plugins/tmux-pain-control)
* `vim` with custom config and few basic plugins like *vim-sensible*

## Motivation

The original motivation was simple: at work, I often need to copy the commands I run + their output, as part of the code change test plan,
or incident investigation timeline.

Since I used a one-line shell theme *with* the time and VCS info in the right corner, the text I copied included this info which I then had to remove for clarity.
Having the current time in each shell prompt is quite important, as it makes reconstructing the timeline of the executed commands very simple.
And having a VCS info in your prompt is practically a necessity nowadays.

Obviously I was not ready to cram both into the left side of the prompt, that would be quite inconvenient.

The solution I came up with was using a two-line theme, but building a custom one is too much effort, plus I wanted to see what fellow engineers are up to in the year 2024.

And since I got into the weeds of modern CLI setup, why not look at other stuff too?

## Shell

At first, I looked at Fish Shell once again. I used it for two years back in the days, and [dropped because lack of POSIX-compatibility is just too annoying](/it/fish-zsh/).
While since 2016 Fish made good progress in becoming closer to the POSIX-compatible shells (with adding `&&`/`||` for example), I still couldn't cope with the other quirks.

Back to zsh then, just with a different theme!

I ended up trying quite a few prompts, including interesting approaches like [Starship](https://github.com/starship/starship), but ended up with [powerlevel10k](https://github.com/romkatv/powerlevel10k).

The reason was simple - latency.
In the case of *Starship* for example, while the idea of a cross-platform, compiled prompt is interesting, paying the cost of spawning a process (or multiple) each time is just absurd to me.
Also, saying it's "really really fast" in the readme, but providing no proofs or benchmarks - that's lame, and there is even an [issue open for this](https://github.com/starship/starship/issues/5593).

*Powerlevel10k* won because it is native zsh, and is [heavily benchmarked](https://github.com/romkatv/zsh-bench), which is what I consider a proper scientific approach to the shell prompt latency problem.

My new theme is similar to the old one, just split over two lines. Works a charm, and if necessary, I now have access to the more advanced plugins that powerlevel10k provides.

Original theme:
```
~/g/abulimov.github.io ❯                                    sources ✱ ◼ 21:38:16
```

New one:
```
~/github/abulimov.github.io sources !1 ?1                               21:38:16
❯
```

As you can see, it provides more information about the path and VCS status while allowing for easy copying of the command+output.

## Terminal multiplexer

I've been using tmux since times immemorial.
Not a lot of competition in this area, I have to admit.

Still, a new option appeared since 2016 - [Zellij](https://zellij.dev), and of course I gave it a spin.

The mere fact that there is now a new, interesting, actively developed, and written in a sensible language terminal multiplexer genuinely makes me happy.

And it's very pleasant to use - configurable, fast, user-friendly. It took me only a few minutes to tune the UI a bit and make it look and behave just like I want.
The obvious advantage against `tmux` is how everything is a pane, including the status and tab bars, and so the layout is fully customizable.
And on top of this, Zellij has advanced plugin support.

The only problem so far - I found no use for all those advanced features, and ended up with it looking and behaving like `tmux` with pain-control.
And I can already have all I need with tmux, which I can also easily install on any system I ssh into.

So while I found Zellij to be very nice and even exciting, I couldn't (maybe yet?) find one reason to replace `tmux` with it.

I will continue experimenting with Zellij on my home machine, since I already made it quite comfortable, while still using tmux at work.

At least after this experiment, I refreshed my tmux config by switching to a [*catppuccin* theme](https://catppuccin.com/) and adding a hostname into the status line (so that I can drop it from the shell prompt), so it looks quite modern now.

## Editor

Ever since the early days of my SysAdmin career, I've been a `vim` guy. For a SysAdmin, it has the added benefit of being present pretty much anywhere - even the most dated and forgotten system will have at least the basic `vi` on it.

That alone means that I have about 15 years of muscle memory for vim key bindings and motions.
And while editors like [Helix](https://helix-editor.com/) or [Kakoune](https://kakoune.org/) are most definitely interesting in the way they try to modernize the modal editing, for me the burden of re-learning the motions is just too big.

Still, experiments with Helix showed me how cool and user-friendly a modern terminal-based editor can be, with LSP support, floating windows and linter suggestions working out of the box.

Sure enough, it turns out that all of this (and much more) can be easily achieved with NeoVim!

Like with zsh, I found it easier to find a well-supported pre-made configuration that I can tweak to my needs, rather than building my ideal config from scratch.

In case of NeoVim I settled on [AstroVim](https://astronvim.com/) which provided sane defaults and proved to be a good staring point.

Mind you - I don't use NeoVim for coding at work, only for small pet projects, configs, and this blog.

Given that a relatively plain vim config sufficed for this for years, you can see how the default AstroVim setup is a massive improvement.

## New setup

* `zsh` + [zprezto](https://github.com/sorin-ionescu/prezto) with [powerlevel10k](https://github.com/romkatv/powerlevel10k) theme
* `tmux` with [*tpm*](https://github.com/tmux-plugins/tpm), *pain-control* and *catppuccin/tmux*, while Zellij is being evaluated
* `neovim` with [AstroVim](https://astronvim.com/) 

Will it last for another 8 years? Who knows!

Did this research and experimentation improve my CLI workflows? Absolutely!

P.S. while refreshing the configs, I migrated from `homesick` to [`homeshick`](https://github.com/andsens/homeshick) since it provides similar functionality and doesn't need Ruby.
It's been over a decade since I worked in a Ruby-on-Rails shop, and outside of Chef at work I have no need or desire to touch Ruby ever again.
