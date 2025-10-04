---
title: "Repairing a robot vacuum cleaner"
date: 2025-10-04
slug: repairing-robot-vacuum
Categories: [Personal]
tags: [Vacuum Cleaner]
---

I'm pleased to report that modern robot vacuum cleaners are fairly easy to repair, at least from the mechanical standpoint. 

I guess the relatively large form factor allows for components to be big enough, and that there is no clear need to miniaturize everything.

Debugging the robot vacuums from a software standpoint is a completely different affair, and not in a good way. 

In my particular case, my trusty [ECOVACS T8](/post/2023/08/13/robot-vacuum-amazing) developed a problem with one of the driving wheels,
probably after being stuck on a cable or a sock way too often.

In any case, it began to only turn around one side, and became completely useless.

I ordered a replacement wheel assembly from AliExpress for 16EUR with shipping, and in a couple of weeks it got delivered. 

Thankfully, there are few videos of people servicing such robots, so I had no issues getting to the wheels.
Tons of screws to undo though, and at the time I didn't have anything outside a regular screwdriver to help with this process. 

Anyway, I managed to replace the wheel, and put back the bare minimum of the robot parts to verify that the replacement works. 

To my delight, robot was able to move around freely again!

However, it **started to complain about the drop sensor being dirty**. 

That's where the software side of debugging came to light - outside the error in the app,
and the annoying voice announcement repeating the same thing about the 'drop sensor needing to be cleaned', there were zero pointers. 

Why did it frustrate me? Because for one, the robot has six of those sensors, and nowhere could I see which one it was not happy about. 

I struggled with this for a few hours, re-connecting and cleaning the sensors over and over again,
and eventually grew so frustrated that I shelved the half-disassembled robot for a better time. 

In a few weeks, I could no longer look at this lifeless carcass of a vacuum cleaner any more, so I resumed the repair. 

I re-connected all sensors again, and then a bright idea came to me -
**I thought that I could use my phone's camera to see if any of the sensors are not emitting the infra-red light** when the robot was on. 

To my surprise, none of them did!

Quick search on the Internet showed me a reddit thread where a user had issues with sensors after some kind of a problem with the bumper. 

I was puzzled to say the least, since the bumper was one of the last things I planned to connect back,
and was not connected with the drop sensors in any way I could see. 

Still I gave it a try and connected it back. 

To my greatest surprise, I could instantly see (through my phone's camera) all of the drop sensor diodes emitting light.
And when asked to vacuum, the robot happily obliged. 

I was off course rejoiced with this miraculous fix, but again this brought to light just how incredibly easier such repair would have been,
have the robot had any proper debug mode, or some debug software I could use. 

Anyway, this story got a happy ending after all, and with the repair costing me only 16EUR I'm pretty chuffed. 

Granted, after finishing the reassembly I found few extra screws, but that didn't affect the robot functionality at all.

And after partially assembling and disassembling this vacuum so many times,
I bought myself a nice precision electric screwdriver from Hoto.

I simply figured out that in the future if I need to repair it again (which is quite likely),
I won't be able to bring myself to deal with all those endless screws without some help. 
