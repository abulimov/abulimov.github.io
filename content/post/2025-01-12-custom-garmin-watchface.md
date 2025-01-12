---
title: "Writing a custom Garmin Instinct 2 watch face"
date: 2025-01-12
slug: custom-garmin-watchface
Categories: [Personal, IT]
tags: ["Watch", "Garmin", "Instinct 2", "Apple", "Smartwatch"]
---

![watch face](/images/retrosimple_watchface.png)

# The search for my perfect retro watch face

I've been enjoying my [Garmin Instinct 2](/post/2024/10/04/dumber-smartwatch/) a great deal, but after getting a [Casio Royale](/post/2024/10/26/modding-casio-royale/) I yearned to make my Garmin more 'retro'.

I found a great existing watch face called ["7 Segments Simple"](https://apps.garmin.com/apps/b7f055a4-9098-41ed-8c54-92e992a31139) which imitates the look of classic [7-segment displays](https://en.wikipedia.org/wiki/Seven-segment_display).

It was *almost* perfect for me, except that I wanted to see the current weather right on the watch face.

Since I found no source code repo for this watch face to contribute this feature, I decided to play with Garmin's **Connect IQ SDK** and build my own, similar watch face.

After all, the API seemed very simple, and customizing my watch by coding is right up my alley.

*Tangent: rant about Apple Watch*

Speaking of customizing a smartwatch...

One of the things I really found lacking with the Apple Watch was being able to fully customize it.

Just to make it clear, there are a couple of really serious obstacles to building *anything* for iPhone/Apple Watch:
* one needs a macOS system to build any mobile app (hate this limitation with passion).
* in order to get a dev licence that allows publishing apps, one needs to pay the greedy multi-billion company 99 USD per year.

Both are annoying enough for me already...

But the main answer to the question of "why I didn't create a custom Apple Watch face?" is even simpler:
Apple forbids creating fully custom watch faces, and even goes as far as banning any app looking like a watch face from the App Store.

Very developer-friendly and not annoying at all...

*Rant end*

## Development process

It took me only couple of hours to get familiar with the SDK, the API and Garmin's extension for VS Code.

The SDK comes with a watch emulator, so testing the code is as streamlined as it gets.
Really quick iteration cycles, when building and testing a watch face only takes few seconds.

The language Garmin uses is called [Monkey C](https://developer.garmin.com/connect-iq/monkey-c/), and it is a C-like duck-typed language that is compiled into byte code.
Nothing special, but it's good enough for the task at hand.

Instead of painting the segments as polygons (my original plan), I found a beautiful font called [DSEG](https://www.keshikan.net/fonts-e.html).
Garmin watches support using custom fonts, which allowed me to simply write any text styled as a 7-segment or 14-segment display on the watch screen.

It proved to be a great approach, and allowed me to build the first prototype in one hour.

From there it was simply a matter of migrating to "layouts" (XML files describing the elements, customized for each physical screen size) to add support for different watch models (normal and small versions of Instinct 2 for now), and the first version of the app was ready.

By the way, side loading it into my watch was as simple as copy-pasting it over USB.

### Refreshing every second

The only tricky part in the whole watch face development process was dealing with the partial display updates to enable seconds 'ticking' while the watch is in energy efficient state.

Thankfully, the trick is [well documented](https://developer.garmin.com/connect-iq/connect-iq-faq/how-do-i-get-my-watch-face-to-update-every-second/) and basically boils down to defining a `onPartialUpdate` function and inside it setting the screen clipping to only update the seconds area.

### Debugging

I used my new watch face for a good few days before encountering a crash.

Debugging proved very easy - the crash log (with a full stack trace, if the app was built in a development mode) is stored on the watch, and accessing it is again done over the USB.

Turns out, I didn't handle the fact that the weather could be 'null' in some cases, duh.

## Publishing the app

Publishing my watch face was rather simple too. Use one command in VS Code, upload the file into a web form, wait for the review, and [that's it](https://apps.garmin.com/apps/516e843d-6d26-4f48-9760-3d01989872c6).

No need to have a specific proprietary OS. No fees. And there is even an input field for the app source code repo!

Did I mention that my watch face is fully [open-source](https://github.com/abulimov/garmin-watchface-retrosimple)?

I'm a big proponent of open-source, it was only logical to make the watch face open under the MIT licence. If anything, it might be useful for someone to copy-paste some code in their own custom watch face.

## Conclusion

That was a fun little project. I'm quite happy with the outcome, and use my custom watch face exclusively.

Was the time investment (which I estimate around 4-5 hours) worth it? To me, the answer is a resounding "yes", since I got to tailor my watch experience exactly to my current needs.
