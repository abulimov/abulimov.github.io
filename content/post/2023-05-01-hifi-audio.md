---
title: "My Journey to HiFi audio"
date: 2023-05-01
slug: hifi-audio
Categories: [Personal]
tags: [HiFi, Audio]
---

This year I upgraded my audio setup, finally bringing it to the quality and convenience level that I'm happy with, and this positive change prompted the reminiscence.

## 2000 - Humble beginnings 
Funny enough, my journey to HiFi audio started with no audio. I had a CD-ROM drive in my first PC in 2000, and back then CD-ROM drives had headphone outputs. I used it to play *Dark Side of the Moon* by Pink Floyd through the cheapest no name earplugs, and was completely floored by it.

I did it this way because I couldn't make the computer speakers work with audio CDs, and had no other means of playing audio CDs.

I recall using this option for quite some time, even after I fixed playing music through computer speakers.
The reason was simple - cheap computer speakers were rather terrible in early 2000s. They were tiny, milky white plastic things that sounded as bad as they looked, and made funny noises when mobile phone rang next to them.

## 2007 - Microlab speakers
Around 2007 I started to make some money. I was already studying in the university, so earned money by helping other students with coding tasks.
This allowed me to buy *fancy* (at least for a student at that time) **[Microlab](https://en.wikipedia.org/wiki/Microlab) Solo 6C** speakers - big, wooden, HiFi-looking with tweeters and mid-range drivers. They looked the real deal, and sounded nice enough.

Soon after buying them I realized that having big and powerful 100 Watt speakers is very far from practical when you live in a tiny 8 square meter room.

This realization finally made me start looking at high quality headphones.

## 2009 - Consciously choosing headphones
Up until 2007 I paid no attention to headphones I used. Mostly it was cheapest headphones bundled with portable cassette (later CD) player, or something similarly cheap bought for a replacement.

I remember one day listening to **Koss Porta Pro** that one of my university peers had around 2006, being amazed by the bass and the sound in general. But Porta Pro were expensive, I was poor, so I never bough one for myself.

Finally around 2009 I was gifted **Sennheiser IE4** in-ear monitors for my birthday (which I picked, but couldn't make myself buy - they were rather expensive).

Those were absolutely delightful, and served me well for years, up until 2016 or even 2017. Their neutral sound was a perfect match for prog rock I was very into at that stage.

## 2013 - First good big headphones
I was kinda set with portable headphones since I've got IE4s, but work headphones were completely different thing. Various cheap over-the-ear headphones I had were terribly sounding and didn't last long (which was probably a good thing).

As usual, I gave the matter of choosing proper big headphones a great deal of thought, read reviews and forums, and settled on proved, respected brand - **Audio Technica**.

All of my friends chipped in, and bought **ATH M50** for my birthday in 2013. I enhanced it with external USB audio card - **SoundBlaster X-FI HD**. I did it after the basic testing - surprisingly, even in 2013 PC sound cards were mostly garbage, it was easy to hear the difference.

This new setup was such a game changer for me. Neutral and detailed sound of M50 allowed me to appreciate the complicated prog rock records on a new level, and ATH50 proved to be extremely well built and are still very much alive to this day.

## 2018 - Raspberry Pi experiments
I kept the SoundBlaster + ATH M50 combo for almost 10 years, changing only the sound source.
At some point, I set my mind on reducing the distractions that playing music from a laptop provides. I wanted to achieve this by building a headless standalone player based on Raspberry Pi and [MPD](https://github.com/MusicPlayerDaemon/MPD) + a web-based UI, of course with good old SoundBlaster for audio output.

I wrote software in Go that allowed me to control MPD with physical buttons and display player data (current song, playback status) on a 2x16 screen attached to Raspberry Pi 3 GPIO, and assembled everything on a breadboard.

It was great fun dealing with wiring and hardware, and it all worked rather well.
But when I looked into turning this setup into a real product, I realized that it's just not appealing to me. Designing the case, soldering everything - I remember how long this stage takes based on my previous Arduino-based projects, and just didn't want to invest so much time and effort.

In the end, the project got shelved and I was stuck with playing music from laptop.

## 2023 - Current setup
Back in 2019 I had an opportunity to buy **Sennheiser HD6XX** from Massdrop (now Drop). I was intrigued by the promise of open-back headphones sound scene, and the price was good.

I liked their sound quite a lot, but lack of any sound insulation inherent to the open-back design, and 300 ohm impedance that mandated the use of a headphone amp limited the opportunities to enjoy them.

I was still limited by using SoundBlaster X-FI for the amplification, and it needed USB-A connected to a laptop to play music - not the most convenient setup. At least for me, bringing a laptop with USB audio card to a chair or a bed for an album spin is far from ideal (but I still did it) .

It annoyed me that I have such great headphones that I rarely use, and finally few months ago I rewarded myself with a proper headphone amp, so that I can use any sound source with **HD6XX**.

I settled on basic but good **Topping L30II** amp, which proved to be perfect for my use-case - small, great build quality, and most importantly great sound quality and enough power to drive any high-impedance headphones.

I use iPhone as a sound source, mainly because it's the most convenient way to listen to various music (thanks to streaming services), but also because I cannot hear any difference between its lightning-to-3.5mm dongle DAC and other DACs like laptop audio cards.

To sum it up, this is the current setup that leaves me very satisfied:
* **iPhone** with Apple Music/Bandcamp and 3.5mm dongle
* **Topping L30II** headphone AMP
* **Sennheiser HD6XX** open-back headphones

While for work I use **Sony WH-1000XM3** wireless over-the-ear headphones because of their excellent noise cancellation and decent audio quality.

The difference between Sony and HD6XX is pretty significant (even my old ATH M50 sound better than Sony), so whenever I really mindfully listen to music - I do it on HD6XX with an amp conveniently plugged into the iPhone.
