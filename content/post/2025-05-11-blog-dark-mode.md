---
title: "Added Dark Mode support"
date: 2025-05-11T16:00:00
slug: blog-dark-mode
Categories: [Personal]
tags: [Blog]
---

Now this blog supports Dark Mode, if the browser has it set as preferred.

I myself switched to using Dark Mode on some of my devices, but only recently noticed that my very own blog didn't have the support for it.

Thankfully adding it was super easy, and I didn't need to go much further than this blog's theme Issues on Github.

The author of this lovely [`xmin`](https://github.com/yihui/hugo-xmin) theme provided an answer in the [issue #67](https://github.com/yihui/hugo-xmin/issues/67):

```
@media (prefers-color-scheme: dark) {
  body {
    background-color: white;
  }
  html, img, video, iframe {
    filter: invert(1);
  }
}
```

I added this in a custom header partial override, and voilà! Nice enough dark mode, at least in my opinion.

Enjoy!
