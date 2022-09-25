---
Title: How I became a programmer
Date: 2016-09-30
Tags: [Programming, Experience]
Categories: [Personal]
Slug: how-i-became-a-programmer
Url: personal/how-i-became-a-programmer
---

After reading a lot of blog posts about becoming a programmer recently, I've decided to write my own.

It will be a bit different because of two factors:

* I'm not a Software Engineer, but a Production Engineer/SRE/Admin;
* I'm from Russia, where CS education is vastly different.


## School years

*School in Russia is 10 or 11 years and you start at the age of ~7  and end it at ~17*

As far as I recall, my first programming experience was with
[LogoWriter](https://en.wikipedia.org/wiki/Logo_(programming_language)) in elementary school.
I wasn't bad at it, and even enjoyed it a lot, but our LogoWriter course ended quite fast,
and since then I can't remember anything useful related to programming in my school courses.

As you may imagine, personal computer was not a common thing in 90th in Russia,
so in my family it appeared only in 2000. The fun thing I remember about using Windows 98 first time
was me calling my mom and asking if I will be able to open a program again after I close it.
For me, 'closing' was like shutting down some factory.

Anyway, approximately during 9th year of school some boys in our class were attending some
external paid programming courses, where they were using
[Borland Delphi](https://en.wikipedia.org/wiki/Delphi_(programming_language)).

Obviously they've shown other students some of their programs, so I've tried to write something in Delphi on my own.
No surprise, I haven't written anything and became absolutely sure that programming is not my cup of tea.

**So during school I developed only strong feeling that programming was to hard for me**

## University

During school years I was quite good at math, and not very good at physics,
so I decided to attend Applied Math Faculty of Moscow State Technical University of Civil Aviation.

Very soon I've discovered that

1. There is a LOT of physics in Applied Math program;
2. I don't like all this Calculus courses at all.

And in Russian university you can't select or change courses once you've chosen your Faculty.
So every Faculty has pre-defined selection of various courses, all of which you must attend
and complete. At most you can change your Faculty, but it's a very difficult and painful process.

This system is quite stupid, as you have to learn all the stuff you don't like at all,
and all the stuff that you don't need at all. For instance, I have to attend and complete
some strange courses related to Civil Aviation, like 'History of Civil Aviation' and 'Economy of Civil Aviation',
some useless crap about Sociology, and many other useless courses. And everybody knew that this courses was useless,
nobody enjoyed them, but all of us had to complete them.

And what's worse -  you can't attend courses in your university that you are really interested in
if they are not in your Faculty program.

Anyway, on our first year we had a lot of basic Borland Pascal programming classes, and I really enjoyed it.
By the end of the semester I was making money doing homework for other students
(as you can't really skip any courses in Russian university, you have to complete them somehow,
so it's a very common thing to pay for homework).

During all the University years I was making money doing various programming tasks and studies for other students,
so I sort of hacked the system and was able to 'attend' in some way other Faculty's courses. I even remember
writing an 'engine' in C++ to draw various 3D figures using DOS VESA driver for other Faculties, because I've got so
many orders from them that writing proper engine able to draw figures described as polygons in a simple text file
was easier than writing every project individually.

First two years we were learning some basic procedure-oriented programming in Pascal, and it wasn't that bad,
as it was my intro to programming and I learned a lot. I even recall implementing some simple algorithms,
like bubble sort.

Then, on third year we had a course called "Operating System basics" or something like that.
It was taught by [Andrey V. Stolyarov](http://www.stolyarov.info), very bizarre person, fanatic of Open Source
and C programming language. Despite all his oddness this course (which described Unix operating systems
and Linux kernel) was extremely good, and I had some really hard (but fun) time wrapping my head around C, pointers,
references, memory management and sockets. The course basically made us write chat client and server step-by-step,
and I was one of the few who actually accomplished this goal. It was very useful, I learned A LOT about operating
systems and low level stuff, and used Linux first time. And [K&R The C Programming Language](https://en.wikipedia.org/wiki/The_C_Programming_Language) is still one of the best IT books I've ever read.

Next semester the course continued with C++,
and we've been implementing lots of data structures from [STL](https://en.wikipedia.org/wiki/Standard_Template_Library).
As I continued making money on other student's homework, I've implemented all basic data structures,
including linked lists, vectors and binary trees. It was extremely helpful and insightful, I learned about all
common data structures and algorithm complexity. And I learned about Object Oriented Programming and C++ templates.
It was all new to me, and of course I became a fan of OOP.

Later, on fourth or fifth year, we had something about Relational Databases, and used [LAMP](https://en.wikipedia.org/wiki/LAMP_(software_bundle)) to build some basic [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) interface.
I've learned about [normalization](https://en.wikipedia.org/wiki/Database_normalization), JS and CSS, but the most
important thing was that I've finally realized that I wasn't the best in programming in the class - two students were
better programmers than me.

**So university gave me A LOT. It basically introduced me to programming, gave a strong basic knowledge,
and even gave me a quite good overview of Unix-like OSes. But it also made me think I'm not good enough
for Software Engineer job.**

## First job

Realizing that I wasn't the best programmer in the class somehow made me think that Software Engineer
career is not for me, so during my fifth year I attended a job which we call in Russia 'AnyKey'.
Basically it's the first level of IT helpdesk, but in my case it was a small company, so I was doing everything.

My work PC was some old notebook with Windows XP, and it took 11 minutes to simply boot OS. I was very tired of it,
and ended up using Ubuntu 10.04. It worked really well, so I started to learn Linux and master bash and console tools.

My job included maintaining some basic [Proxy Server](https://en.wikipedia.org/wiki/Proxy_server) on Windows XP.
Obviously this thing was illegal and unstable, so I've assembled another PC from spare parts and set up OpenSuSE 10
on it, because it has very nice graphical configuration utility for almost everything - YAST.

This led to using more Linux-based tools and servers, and I ended up re-implementing some really big and complex Excel
spreadsheet as a LAMP-based service. The code was absolutely terrible, as I didn't know about [MVC](https://en.wikipedia.org/wiki/Model–view–controller),
so it was a mess of HTML and PHP with tiny bits of JS for AJAX. But it was my first experience of programming
in a new domain and trying to implement something that other person vaguely wanted.

**So my first job gave me some real-world experience, a lot of Linux-related experience. I've learned bash
and started to use Vim.**

## Second job

So I mastered bash, used some PHP, and after a year my company was bought by bigger company, so I've moved to bigger IT
department. At this point I was fluent with bash and terminal, but wasn't programming anything real.

In my new company I was dealing with some IP phones, and decided to implement shared phone directory for all
phone models we have had. This time I new about MVC, so used [Yii](https://en.wikipedia.org/wiki/Yii), and
the code was not that bad. I accomplished the goal of having universal phone directory with nice web-ui,
but have not open-sourced it as I just hadn't time to make proper installer. During this project I learned how
to use MVC properly.

Around same time I decided to use [Chef](https://en.wikipedia.org/wiki/Chef_(software)) for all configuration
management, so I learned a bit of [Ruby](https://en.wikipedia.org/wiki/Ruby_(programming_language))
and started using [Mercurial](https://en.wikipedia.org/wiki/Mercurial) for revision control.
It was very cool to finally discover modern dynamic languages, which were very different from my PHP experience.

**So my second job gave me even more Linux-related experience, I've built normal app using MVC pattern,
and I've finally tried modern dynamic language.**

## Third job

Eventually I became bored being just a SysAdmin, and moved to a startup where I could be
something more - they called it 'DevOps engineer'. In this company I've switched from Chef to
[Ansible](https://en.wikipedia.org/wiki/Ansible_(software)), and learned
[Python](https://en.wikipedia.org/wiki/Python_(programming_language)) to fix a bug in a module I was using.
It was my first contribution to Open Source project, which I was very proud of.
I've been missing some modules in Ansible, so I just wrote them and contributed to upstream.

I've fallen in love with Python and continued to use it for various monitoring scripts.
At the same time I've started to use unit tests, as my company was a Ruby shop, and all Software Engineers
relied on unit and functional test heavily. I was impressed how helpful it was, and became a huge fan
of automated testing and [CI](https://en.wikipedia.org/wiki/Continuous_integration).

A year later I've learned about [Haskell](https://en.wikipedia.org/wiki/Haskell_(programming_language)),
and as person with Applied Math background I was extremely interested. I've bought
['Learn You A Haskell For Great Good'](http://learnyouahaskell.com), read it,
and even written some basic games like Tic-Tac-Toe with AI.

It introduced me to functional programming, but I wasn't be able to write anything big and useful in Haskell.
But it gave me the understanding of how much a good typing system with good compiler can give a programmer
in terms of reliability and catching most of bugs *before* executing code.

**So my job at startup gave me a lot of programming experience, I've started to use Python, auto testing and CI,
learned about functional programming, and fell in love with modern static typing.**

## Fourth job

After the startup I was working at became a bankrupt, I had to find another job.
It was surprisingly easy, and I became a Production Engineer in online cinema.

At this company I had a lot of great non-standard tasks, so I've been using my programming skills a lot.

Initially, I was using Python for everything, as it was my language of choice, but I was interested in trying
[Go](https://en.wikipedia.org/wiki/Go_(programming_language)) with it's great concurrency support
and static typing.

Luckily, one of my monitoring tasks required a good amount of concurrency, so I just wrote it in Go.
It was surprisingly easy, static typing was very helpful, and the tooling around language was very good.
Since then, I've continued to use Go more and more, and wrote some relatively big programs in it - like
my [linter for HAProxy configs](https://github.com/abulimov/haproxy-lint).

About this time I've started to use [Atom](http://atom.io) text editor, which is written in JavaScript,
so I ended up developing a couple of plugins for it using CoffeScript and JavaScript. I had no illusions about
JS after using dynamically typed languages for a long time, but I was very surprised by the tooling around this language.
It appeared to be extremely good and far superior to the one Python has.

**So my fourth job gave me a lot of opportunities to develop things in languages of my choice, so I've got
a lot of experience developing tools from scratch. Also I've learned Go and tried JS.**

## Fifth job

Now I'm dealing with some complex systems, mostly in Python, and quite happy with it. I am surrounded by very smart
people and have enough challenges for many years.

## Conclusion

After getting solid basic knowledge in the university, I was learning only by myself. And even in the university
I was studying a lot of other Faculties courses material on my own to do their homework for money.

And for me, the only reasonable way to learn by myself is to be surrounded by smart people and to have tasks that
are more difficult than what you can handle right now. I've always had some challenging tasks,
and when my job stopped being challenging, I've changed it.

And while I've been learning new programming languages, as an SysAdmin/SRE I was able to switch them easily
without loosing value as a worker, so I was learning more general things and not some particular language quirks
and bizarre tricks.
