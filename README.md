# Fancy e-ink photo frame

### A project to build a nice 10.3-inch grayscale e-paper picture frame that updates once a day.

https://github.com/user-attachments/assets/95cea70d-8090-42fa-a7ea-d0496e093b6a

For years I've been intrigued by the unique aesthetics of e-paper displays.  A changeable surface that doesn't emit any light, and can display a static image perpetually?  Wouldn't this kind of display be great for showing art?

## Parts list:

<img src="documentation/pizero2wh.png" style="width:50%;max-width:256px;" />

### [Raspberry Pi Zero 2WH](https://www.adafruit.com/product/6008)
* Wifi, bluetooth, micro-SD slot
* GPIO header pins included
* Relatively flat shape (for going behind a frame!)

<img src="documentation/display.png" style="width:50%;max-width:256px;" />

### [10.3-inch e-Ink display](https://www.waveshare.com/10.3inch-e-Paper-HAT.htm)
* 1872x1404
* 16 shades of grayscale
* 1 second refresh time (but could be a whole minute for all I care)
* Just the raw display.  Careful!  Very fragile without an enclosure!

<img src="documentation/display_hat.png" style="width:50%;max-width:256px;" />

### [Waveshare e-Ink display Hat](https://www.waveshare.com/10.3inch-e-Paper-HAT.htm)
* Included with the display
* Several ways to wire it to a Raspberry Pi

<img src="documentation/pisugar.png" style="width:50%;max-width:256px;" />

### [PiSugar 3 portable power supply](https://www.pisugar.com)
* 3.7v 1200mah battery
* Internal clock
* Low-power mode with a wake up alarm to turn on the Raspberry Pi
* USB-C charging

<img src="documentation/pisugar-6_pin_connector.png" style="width:50%;max-width:256px;" />

### [6-pin Molex Connector Cable, 1.25mm pitch](https://www.adafruit.com/product/4926)
* Wires included
* This fits the aux connector on the PiSugar 3

<img src="documentation/piuart.png" style="width:50%;max-width:256px;" />

### [PiUART - USB Console and Power Add-on](https://www.adafruit.com/product/3589)
* For diagnostics when wifi is unavailable
* Cheap
* Handy in an emergency

<img src="documentation/frame.png" style="width:50%;max-width:256px;" />

### [Custom size empty frame from Frame-It-Easy](https://www.frameiteasy.com/frame-styles/ashford?cid=1)
* Art Size: 8 3/4" x 6 3/4"
* Outside Frame Size: 10 15/16" x 8 15/16"
* Style: Ashford, in Gloss Black
* Matting: 1" Smooth Black (White Core)
* Cover: Clear Acrylic

<img src="documentation/usbc_cable.png" style="width:50%;max-width:256px;" />

### [Right-angle USB-C extension cord](https://www.amazon.com/dp/B0BZBRG92Z)
* 0.3 meters
* Makes it much easier to charge the battery

<img src="documentation/wire_caps.png" style="width:50%;max-width:256px;" />

### [A heap of wire caps and a crimping tool](https://www.amazon.com/dp/B0CYNYJTKD)
* No soldering in this project
* Way more than I need, but oh well

<img src="documentation/jumper_cables.png" style="width:50%;max-width:256px;" />

### [A pile of short breadboard jumper wires](https://www.amazon.com/dp/B0CNXLLNGN?th=1)
* No soldering needed
* Way too many for this project, but I guess I have spares now

## You will also need:

* Some tape
* An x-acto knife or similar very sharp thing
* A slotted screwdriver
* __A Dremel tool or other means of grinding down metallic material!__

As the instructions below will show, the display board that comes with the e-ink display has a giant connector and pins on it that you don't need, but that add a lot of thickness.  To make the component fit nearly behind the frame you're going to need to _grind these things down to stumps!_  It is satisfyingly violent.

You can skip that step if you want, but you'll need a thicker frame, or it won't hang flat on a wall.  That might not bother you either, though, if you plan to prop the frame on a desk or nightstand.

