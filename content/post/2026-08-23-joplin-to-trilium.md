---
title: "Moving from Joplin to Trilium for note-taking"
date: 2026-08-23
slug: joplin-to-trilium
Categories: [Personal]
tags: [Trilium, Joplin, Diary]
---

Back in 2021 I [wrote about my note-taking setup](/post/2021/05/23/taking-notes/),
and described how I settled on [Joplin](https://joplinapp.org/) at the time.

However, I moved to [Trilium](https://triliumnotes.org) about 6 months ago, and will explain why in this post.

## Brief description of my note-taking setup in Joplin

Since then until beginning of 2026 I kept using Joplin for all my personal notes:

* daily diary
* notes on my pet projects (mostly [scale models](//models.bulimov.me))
* documentation on the house - what we did, what paint is used where, etc
* list of all the international travels we did
* list of stuff I own or want
* list of stuff I did, or visited, or attended, such as concerts
* address book for postcards
* random thoughts, ideas and stuff
* mini-reviews and ratings of:
  - books I read
  - music albums I enjoyed
  - video games I played

I organized my notes as follows:
* one diary note per year, where I keep adding sections to the top,
separating each day with a date header
* one review note per year per category, separating each entry with a title header
* individual notes for projects
* individual notes for all the lists
* individual notes for most of the other things

And this setup worked pretty well for over five years in Joplin,
and about nine years prior in Evernote.

## Problems with my setup in Joplin

Despite this approach serving me well for years, it was time for a change.
With me being better at keeping my diary, and in general at writing down my thoughts,
few issues popped up.

**First and foremost, using massive notes per year per category.**

They are perfectly fine to add to, or to process programmatically.
But finding specific stuff there when reading is a pain.

For my mini-reviews it was okay-ish, since the notes tended to be still somewhat manageable,
and easy to search.

But for the diary it was pretty much write-only, at least on mobile.

**Second, as I wrote more and more, and started to better document my pet projects,
the whole issue of hierarchy and attachments became more prominent.**

Me adding photos of the stuff in my collections, or trying to arrange all the files
I need for a particular project, became a bit of an issue with Markdown.

## Finding a solution

I started to seriously look into the matter of note-taking early this year,
and of course brought this topic up with my colleagues.

One of them kindly pointed me towards the [PARA method](https://fortelabs.com/blog/para/),
and Trilium as a tool to implement it.

Ultimately, PARA didn't work out for me, although I picked a few ideas from it.
But Trilium sure did!

*And for the record, I also tried Obsidian and Logseq.*

## Why Trilium

Since 2021 my requirements to note-taking didn't change that much.
I still wanted (taken from my [Joplin post](https://joplinapp.org/)):
* Desktop app with Markdown support and import/export options
* Simple mobile app to add/edit notes
* OpenSource

What changed is that I cared much less about "Synchronization via Dropbox, that is notes are just `*.md` files in a dedicated directory."

And of course two new items got added:
* streamlined daily diary entries, one per day
* support for deeper hierarchies and arbitrary file attachments

When I did my initial research, I quickly learned that Trilium matched my requirements almost perfectly:
- [x] Great desktop app
- [ ] No official mobile app, but a great web-UI
- [x] OpenSource
- [x] Calendar for the diary, and a button to create/open a note for today
- [x] Arbitrary hierarchy, file attachments

At that point, I was happy to just have a readable, easily navigable diary.
What Trilium gave me surpassed my wildest expectations.

But first, let's talk migration.

## Migrating from Joplin to Trilium

*Brief note about self-hosting:
I host Trilium on my NAS, in a Docker container - nothing fancy.
Thanks to TailScale I can access it even outside my house without exposing it to the internet.*

Now, the migration itself!

Notes stored by Joplin are simply Markdown files, albeit with funny names.
In my case, they were simply stored in Dropbox.

Joplin also has export functionality.

Trilium on the other hand has import functionality, both individual notes and zip
archives.

So in theory, the migration is as straightforward as it gets.

However, since my most important notes were in massive `.md` files per year per category,
I needed a way to split them into notes first.

Of course, it was only a matter of writing a basic Python script.
Which worked a charm for my reviews, but no the journal/diary - Trilium
didn't properly recognize my imported entries, they didn't show in the calendar
despite having correct hierarchy.

That was what prompted me to learn about [Attributes and Labels](https://docs.triliumnotes.org/user-guide/advanced-usage/attributes),
and figure out that the 'real' diary entries must have certain labels.

This discovery lead me to the next two, which blew my mind:
* Trilium has a native scripting support, including applying bulk actions to the notes with JS code
* Trilium has an API, with [Python bindings](https://github.com/Nriver/trilium-py)

I used bulk actions to set proper labels and relations on my diary entries,
and was quite satisfied with the result.

Then I spent a couple of months simply using Trilium as I would use Joplin before,
enjoying the streamlined way to write my journal entries, and separate review notes
for each book or video game - it already made my life so much better.

Once I was sure that Trilium is the way to go, I began to explore its more advanced features.

## Advanced features of Trilium that I love

### Map

First, I wanted to leverage the ['Map' note type](https://docs.triliumnotes.org/user-guide/collections/geomap), and show all our trips abroad
on the world map.

I wrote a Python script that parsed our trips from the single list I kept them in,
and fetched GPS coordinates for each city using Nominatim API.

Then, for each city it created a child note in Trilium with 'geolocation' label set to those coordinates,
and once the script was done all our travels became visible on the map.

That alone was so satisfying!

### Collections

Then I discovered other [collections](https://docs.triliumnotes.org/user-guide/collections), namely Table.
It made me realize that I could completely revolutionize how I record my mini-reviews.

By using inherited [Promoted Attributes](https://docs.triliumnotes.org/user-guide/advanced-usage/attributes/promoted-attributes),
I was able to make sure each review note has a *score* attribute, which then allowed:
* Table per year that shows title and score, with ordering so I can easily see my top-rated titles
* Programmatic way to fetch score for each review without parsing the text (used to export scores to [this site](/reviews/))
* Programmatic way to validate my Trilium data to make sure I didn't forget adding a score to a partially written review

### Cloning

Any note can be 'cloned' to multiple places in the sub-tree, which enables even more cool things.
Once I got the hang of attributes, I realized that I can re-work my list of video games I own into a sub-tree,
where some notes are shared with Reviews sub-tree.

Now instead of having multiple lists, I have a sub-tree of notes having certain promoted attributes, like
score, genre, platform and status. Whenever I acquire a game, I add it into this Inventory sub-tree with
no score, empty note text, and attributes like platform, genre and status populated.

Once I start playing and forming my opinion, I begin writing my review in the same note, and 'clone' it into the appropriate
Reviews sub-tree. And once I'm done, I update the *status* and set the *score* attribute accordingly.

### Saved Search

I set up 'Saved Searches' to see video games that I own sliced by platform or status.
For example, I have a search called 'Games to play' which only shows games that I haven't finished or dropped yet.

### Note relations

I have a small set of notes about people in my life, where I keep list of potential and past presents, important
events, etc.

Notes in Trilium can have relations like 'isPartnerOf' which makes keeping track of such data even easier.

### Note revisions
Trilium has built-in capability of keeping note revisions, so for each note I can see the history of edits,
and if necessary revert to the previous version.
Dropbox can also do that for some files, but here it comes out of the box, with an easy interface providing diff view.
Loving it.

### Attachments
Any note can have multiple attachments, used for embedding images, or just adding anything to the note.
I use them both for diary (pictures of notable things), and projects (anything from scripts to images or 3d models).

### Encryption

Any note or sub-tree can be 'protected', encrypting them. I don't store passwords in Trilium, but some people do.
Still, I 'protect' my diary and other sensitive sub-trees, just so that the data is encrypted on disk.

## It's not all perfect

Trilium is very powerful (and very cool), but there are some downsides, at least for my use-case.

### No official native mobile app (yet)
To be clear, native mobile web UI is very good, but it's not the same.

It seems like there now is an official mobile app in development, which I'm looking forward to trying out.

There is also [TriliumDroid](https://github.com/FliegendeWurst/TriliumDroid), which I tried but didn't like.

And finally there is [PocketTrilium](https://github.com/nriver/pocket-trilium), which I use on a daily basis. The tech
behind it is terrifying, but it works well enough.

### Not as simple as Markdown on disk
Notes are stored as HTML in a database, which of course is much less appealing
than just Markdown. Sure, there is export in Markdown, but the complexity is real.

To be fair, last few versions added more features to work with plain Markdown notes,
so there is hope for people like me.

The data is stored in SQLite, which is not bad at all, and allows for both
inspection and easy backups. But again, not as simple as Markdown on disk.

And of course to sync data between devices you'd better host Trilium server
instead of relying on say desktop app serving as one.

## Conclusion

As of now, I have 3225 notes (2180 of them are my daily journal entries) storing 48 MiB of data.

I couldn't have dreamt of such advanced setup with Evernote or Joplin.

Note (pun intended) that there is nothing wrong with Joplin, and I still
wholeheartedly recommend it for any casual note-taking, and replacing Apple Notes or Evernote.

But now that I know what is possible with advanced personal knowledge base systems,
it would be very hard to go back.

Just in six months I drastically improved my diary keeping experience (and perhaps more importantly
my diary *reading* experience), set up much better system of keeping track of my
reviews and inventory, and beautifully rendered our trips on a world map.

I have no limitations on how I store data and information for my projects,
and my sensitive data is securely encrypted.

To sum up: for my use cases, Trilium is exceptionally useful.
I can't recommend it enough!
