---
Title: Refreshing slow internet experience
Date: 2017-07-23
Tags: [Experience]
Slug: slow-internet
Url: it/slow-internet
Categories: [IT]
---

I've just returned from a vacation, and I've got quite refreshing experience
of using slow internet there.

The thing is, we, as engineers, are used to fast internet, fast development environment, powerful laptops/smartphones, etc.

Unfortunately this is still not the case of a huge part of the world,
and it's really important for us to try and walk in their shoes
from time to time. And one of my colleagues, being fed up with resource-wise inefficiency of modern software, suggested as a joke to use Raspberry Pi as a dev environment.

So returning to my experience - I've been in the Southern Hemisphere,
and tried to access some European and Russian sites. And it was a miserable experience.
Slow and unreliable Wi-Fi + long round-trip made such sites almost unusable,
while Google, Instagram and Facebook were working just fine because of their
Points of Presence close to me.

And in such environment Google's [AMP](https://www.ampproject.org/) showed itself just perfectly. While being [clearly bad from the 'open internet' point of view](https://danielmiessler.com/blog/google-amp-not-good-thing) (and I completely agree with it),
from the 'normal user' point of view it is just what makes his/her favorite sites load fast on bad internet connection.

Because Google caches AMP content and serves it from own servers,
it makes it load from nearest Point of Presence,
and as the content is stripped down to just text + images, it loads instantly, while same non-AMP page takes **minutes** to load.

And this fact makes me think that while anyone can (and should) make their
pages fast, responsive and light, it still won't be as good from user's
perspective, just because it's not feasible for everyone to have caching
POP's close to user.

The page may be just as optimized and lightweight as AMP, but if it's served
from some server that's far from user, Google+AMP will still provide better user
experience, which basically equals being better for user.

It's amusing how this Google's AMP solution reminds me of 90s
with caching proxy servers ([Squid](http://www.squid-cache.org/) anyone?) set up at every ISP.

### P.S.

If you wonder what do people use to actually test their products
on bad internet connection, there are some Open-Source tools to help to simulate whole range of shitty internet issues using `tc`.

For example, on my previous job I've used a simple CLI tool called ['comcast'](https://github.com/tylertreat/comcast) with great success
to test how various SmartTVs behave when playing videos from the internet on a bad/slow connection. By the way, with properly encoded videos, they cope with this task really good.

If you need something more advanced, Facebook Open-Sourced [Augmented Traffic Control](http://facebook.github.io/augmented-traffic-control/), which has a nice Web-UI and Thrift API.
