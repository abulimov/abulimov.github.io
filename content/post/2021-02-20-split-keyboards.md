---
title: "My split keyboards"
date: 2021-02-20
slug: split-keyboards
Categories: [Personal]
tags: [Keyboard, Electronics, Ergodox, Helix]
---

## Intro

Thanks to [RSI](https://en.wikipedia.org/wiki/Repetitive_strain_injury) I'm quite literally forced to use ergonomic equipment.

It's not too bad, and I can use laptop's keyboard and touchpad for few hours a day without much discomfort,
but if I do it for a couple of full working days I get nasty pain in my wrists and fingers.

## How it all started

Many years ago (I believe it was 2014) when I first started to have those symptoms I did a research which lead me to using
**Microsoft Natural Ergonomic Keyboard 4000**, helpfully provided by a colleague of mine.

The mouse ergonomics was easily solved by using vertical mouse from **Evoluent**. It's expensive, but good.

It was an ok-ish setup for a few years, and RSI wasn't too bad so I could use other keyboards mostly fine.
But I was never fully happy with the keyboard, my main grip being the sheer size of it - it's massive, and I have no use for the numpad.

Around 2017 I decided to address the size issue and switched to a newer **Microsoft Sculpt Ergonomic keyboard**.
It had two advantages over the old one - no numpad and split space key.
Unfortunately they messed up the switches. Top row with Esc and F1-F12 keys became completely unusable, with stiff switches
that didn't register the key press about half the times.

And rest of the keyboard got some shitty laptop-like switches, rather unpleasant to use,
which in all fairness were just as bad as mushy membrane switches of the older model.

Being quite disappointed with the upgrade, I looked at commercially available split ergonomic keyboards
just to discover most of them were very expensive and not really good according to reviews.
Also I wanted to address the shitty switch situation once and for all and start using mechanical keyboard.

## Ergodox

After a long research I decided to step up the game, and go for **Ergodox** keyboard. I even found a way to test-drive it,
as I was visiting the US office and one of the colleagues there had it.

So I was fully set on getting one, but there was a catch - it was not easy to buy.
You see, the world of split mechanical keyboards is mostly ignored by big companies,
so most people have to buy PCB, components and quite literally solder their keyboard themselves.
And even the PCB availability wasn't great.

Luckily for me, I was able to get a fabulous **Ergodox Infinity** kit with Gateron Brown switches
from [Massdrop](https://drop.com) (now called simply Drop). It took few evenings to solder it, and about a month to get used to the layout.

![Ergodox wip1](/images/ergodox_wip1.jpg)
![Ergodox wip2](/images/ergodox_wip2.jpg)

But once I did get used to the layout, it was such a massive improvement over anything I ever tried before that there was no going back.

![Ergodox done](/images/ergodox_done.jpg)

Not only the thumb cluster is a great ergonomics feature, but fully programmable nature of the keyboard allows for massive
quality of life improvements. For example, as a long time `vim` user, I was beyond happy with
the ability to use `hjkl` cluster for text navigation everywhere, not just `vim`.

And thanks to excellent [QMK](https://qmk.fm/) firmware I can have up to 32 layers and re-programming is a breathe.

Here is my basic Ergodox layout:

*left hand*
```
+-------+-----+-----+-----+-----+-----+-----+
|   `   |  0  |  2  |  3  |  4  |  5  |  6  |
+-------+-----+-----+-----+-----+-----+-----+
|  TAB  |  Q  |  W  |  E  |  R  |  T  |LCK-1|
+-------+-----+-----+-----+-----+-----+     |
|  ESC  |  A  |  S  |  D  |  F  |  G  +-----+
+-------+-----+-----+-----+-----+-----+ f1  |
| LSHIFT|  Z  |  X  |  C  |  V  |  B  |     |
+-+-----+-----+-----+-----+-----+-----+-----+
  |LCTRL|  `  |  \  |LGUI |LALT |
  +-----+-----+-----+-----+-----+   +-----+-----+
                                    |LCTRL| LALT|
                              +-----+-----+-----+
                              |     |     | HOME|
                              | SPC | ENT +-----+
                              |     |     | END |
                              +-----+-----+-----+
```

*right hand*
```
    +-----+-----+-----+-----+-----+-----+-------+
    |PL/PS|  7  |  8  |  9  |  0  |  -  |   =   |
    +-----+-----+-----+-----+-----+-----+-------+
    |  [  |  Y  |  U  |  I  |  O  |  P  |   ]   |
    |     +-----+-----+-----+-----+-----+-------+
    +-----+  H  |  J  |  K  |  L  |  ;  |   '   |
    | f1  +-----+-----+-----+-----+-----+-------+
    |     |  N  |  M  |  ,  |  .  |  /  | RSHIFT|
    +-----+-----+-----+-----+-----+-----+-----+-+
                |BKSP |LEFT |DOWN | UP  |RIGHT|
+-----+-----+   +-----+-----+-----+-----+-----+
| RALT|RCTRL|
+-----+-----+-----+
| PGUP|     |     |
+-----+ ENT | SPC |
| PGDN|     |     |
+-----+-----+-----+
```

## Helix

I was happily using my Ergodox since 2017 and didn't even look at anything else, until 2020 happened 
and I found myself working from home all the time. And without access to the office where my good old Ergodox was left.

I had to switch back to Microsoft Sculpt keeb, in hopes that either the pandemic will be over soon,
or at least that I'll get the chance to collect things from the office.

Neither of this happened, and after 10 months I gave up and started the research on split keyboards once again.

I didn't want to get yet another Ergodox (first, I already have one, and second, they are really expensive), or anything
very similar to it.

Not much changed since 2017, and again the only reasonable option was getting a PCB, some components and building the keeb myself.

With pandemic it was really hard to even find a place on the internet to buy everything in one order,
but I managed to get my hands on **Helix** kit, again with Gateron Brown switches.

Few evenings of soldering later (I soldered 404 pins if my calculations are correct) I became a happy owner of new split keeb.

![Helix wip1](/images/helix_wip1.jpg)
![Helix wip2](/images/helix_wip2.jpg)

And now after a week of getting used to it I can say that I'm loving it, although still miss few extra keys Ergodox has.
(ignore the labels on the caps, I matched only the alphanums, everything else was placed based on keycap shape, not label)

![Helix done](/images/helix_done.jpg)

And here is the layout I settled on for now:

```
,-----------------------------------------.             ,-----------------------------------------.
|   `  |   1  |   2  |   3  |   4  |   5  |             |   6  |   7  |   8  |   9  |   0  |  _   |
|------+------+------+------+------+------|             |------+------+------+------+------+------|
| Tab  |   Q  |   W  |   E  |   R  |   T  |             |   Y  |   U  |   I  |   O  |   P  |  \   |
|------+------+------+------+------+------|             |------+------+------+------+------+------|
| Esc  |   A  |   S  |   D  |   F  |   G  |             |   H  |   J  |   K  |   L  |   ;  |  '   |
|------+------+------+------+------+------+------+------+------+------+------+------+------+------|
| Shift|   Z  |   X  |   C  |   V  |   B  |  f1  |  f1  |   N  |   M  |   ,  |   .  |   /  |  =   |
|------+------+------+------+------+------+------+------+------+------+------+------+------+------|
| Ctrl |  [   |   ]  |GUI   | ALT  |Space |Enter |Enter | Space| Bksp | Left | Down |  Up  |Right |
`-------------------------------------------------------------------------------------------------'
```

As you can see, I prefer using index fingers and those extra keys next to B/N to switch layers, in both Ergodox and Helix.
I can't stress enough how convenient is to use `hjkl` cluster as arrow keys with a press of a single button.

It took some effort, but now I'm back to being happy with my keyboard and wrist pain is gone.
