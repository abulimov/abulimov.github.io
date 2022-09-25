---
title: "Moved to a new domain"
date: 2022-09-25
slug: moved-to-new-domain
Categories: [Personal, IT]
tags: [Blog]
---

This site just moved to a new domain bulimov.me.
Long overdue move of course, I bought the new domain years ago...

Anyway, the only interesting bit about this is how I'm trying to keep the old links
alive with a little bit of HTML magic.

Using a very basic python script I've created a dedicated github repo
with a directory structure mirroring this site,
where each `index.html` consists of something like this:

```
<!DOCTYPE html>
<meta charset="utf-8">
<title>Redirecting to https://example.com/</title>
<meta http-equiv="refresh" content="0; URL=https://example.com/">
<link rel="canonical" href="https://example.com/">
```

This makes browser open a new link, effectively working as 302 redirect, but without any server side setup.
