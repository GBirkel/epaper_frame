# Fancy e-ink photo frame

### A project to build a nice 10.3-inch grayscale e-paper picture frame that updates once a day.

![Video of the frame in action, with cat for size](https://github.com/user-attachments/assets/2f5732ef-21fd-4f81-a468-279e1d1b35e0)

For years I've been intrigued by the unique aesthetics of e-paper displays.  A changeable surface that doesn't emit any light, and can display a static image without power?  Wouldn't this be great for showing art?

I'm a pretty decent programmer, but when it comes to hardware I'm a novice.  I own a soldering iron but I'm lousy at soldering.  This project went through a few iterations where I tried soldering wires directly onto things and the result was lumpy wires and burned spots on the components.  Eventually I hit on a design that didn't use any soldering at all, just some joining of wires with a crimping tool.  My squinty eyeballs and toasted fingers were grateful.

The software is in better shape.  Driving the e-paper display directly from Python on a Raspberry Pi is complicated, so I went with a sneaky approach:  I modified the freeware demo code published by the display manufacturer.  It's written in C, and all my version does is load an image from storage and send it to the display.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371918833/in/dateposted/" title="2025-03-06-174705-IMG_E6105"><img src="https://live.staticflickr.com/65535/54371918833_9c262918cf_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-06-174705-IMG_E6105"/></a>

All the rest of the code is in Python, and I designed it to do the following:

* When the Raspberry Pi powers up, it checks to see if it's on battery power, or is charging from the USB-C cable.
* It picks one out of the 50% least-recently displayed images from a database on disk.
* It converts the image to Bitmap (BMP) format.
* It calls the C program to display the image, also passing along the current charge percentage of the battery, which is overlaid onto the image.
* If it's on battery power, it sets the PiSugar 3 "wake up" timer to a configured interval, makes sure the wifi driver is off, then powers everything back down.
* If it's charging, it turns on the wifi chip, so the device joins any nearby wifi networks it's already aware of.  Then it goes idle, staying on until someone manually shuts it down (or unplugs the cable and re-runs the Python script)

The history of what image was displayed, and when, and the battery state at the time, is written into the database.

Since I'm using the C program to drive the display, there is no Python display driver.  I'm also driving the PiSugar 3 directly with bus commands, so there's no need to use the PiSugar 3 driver or interface service either.

There are two support scripts included as well:

* `png_inventory.py` scans through a collection of image folders for PNG files, and adds any that are new to the database.
* `register_service.py` can be used to register the script to be automatically launched when the Raspberry Pi is powered up, and to unregister it if necessary 

### Future plans:

There are two additional things I might add here, depending on the direction I want to go:

* Add a web server on the device that launches when it's charging, and can be used to manage the database of images, including uploading new ones and scheduling an image playlist.
* Add a process that runs when wifi is connected, fetching a set of new images and/or an image playlist from a predefined web location.

For now, I just have over a thousand images dumped directly onto the microSD card.  It'll take three years or so to run through them, so there's no hurry to decide which of the above approaches to take...

# Parts list:

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

# Construction

The core of this project is a Raspberry Pi Zero 2WH computer.  Get one, and tear open the box!

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54370809032/in/dateposted/" title="2025-02-11-173800-IMG_5949"><img src="https://live.staticflickr.com/65535/54370809032_e3a38f9ee9_z.jpg" style="width:70%;max-width:512px;" alt="2025-02-11-173800-IMG_5949"/></a>

### Install an OS on the Raspberry Pi

The easiest way to do this by far is with the [Raspberry Pi OS imager](https://www.raspberrypi.com/software/) app.  Install it on your computer, then plug in a microSD card (you may need an adaptor) and launch the application.

I told the app to make a full-featured installation, because with a 16GB media card, why not?  I gave the device the name "pictureframe", and pre-configured it with a running SSH server and credentials to join my local wifi network.

Super-duper easy.  When I plugged the card into the Pi and started it up, it appeared on the local network about a minute later.  Then all I had to do was run `ssh pictureframe.local -l USERNAME` from my computer to log in for the first time.

### Pi can't connect to an unfamiliar wifi? Fix it with the PiUART!

Before we proceed, let's establish a way to connect to the Pi that will work even if the wifi chip is off or there are no known networks around.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371920663/in/dateposted/" title="2025-02-11-191206-IMG_5954"><img src="https://live.staticflickr.com/65535/54371920663_580916c83c_z.jpg" style="width:70%;max-width:512px;" alt="2025-02-11-191206-IMG_5954"/></a>

With the PiUART, you can power and communicate with the Pi directly from a USB port on your computer.

For MacOS, you'll need to enable a serial port in the operating system, which means running some commands to disable "system integrity protection".  If you'd rather not do that, do what I did and use an older version of MacOS in the [UTM emulator](https://github.com/utmapp/UTM/releases).  I had MacOS 10.9 (Mavericks) sitting around, so I used that, and told UTM to just grab the PiUART device directly.

The command to connect to the Pi from there is `screen /dev/cu.SLAB_USBtoUART 115200` and if you'd like to do this in a proper terminal (rather than Apple's plain Terminal app) you can grab an old version of [iTerm](https://iterm2.com/downloads.html).  Set the reported terminal type as "xterm" if you plan to use any fancy semi-GUI stuff.  Hit "enter" a few times after you run the command to wake up the port on the Pi side.

#### How to get your wifi back

All that stuff online about editing `/etc/wpa_supplicant/wpa_supplicant.conf` files no longer applies to the latest OS.  Instead, once you're connected, you can run the `sudo nmtui` command.

(If the interface looks like garbage, make sure you're reporting the terminal as "xterm" in iTerm.)

You can also add and remove known networks directly from the command line.

To add a network from the command line (will auto-join immediately after it's added)

```bash
sudo nmcli con add con-name NETWORKNAME type wifi ssid NETWORKNAME autoconnect yes save yes wifi-sec.key-mgmt wpa-psk wifi-sec.psk NETWORKPASSWORD
```

To remove a network you added
```bash
sudo nmcli con delete NETWORKNAME
```
To list the current known network profiles
```bash
sudo nmcli con
```

### It boots! Now what?

At this point you can try installing the PiSugar 3 through the conventional means, by mounting it to the underside of the Raspberry Pi, like so:

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371682246/in/dateposted/" title="2025-02-11-200318-IMG_E5959"><img src="https://live.staticflickr.com/65535/54371682246_2fcc9bd97a_z.jpg" style="width:70%;max-width:512px;" alt="2025-02-11-200318-IMG_E5959"/></a>

This works great of course, but it makes a stack of hardware that's too tall for fitting behind a picture frame.

There are two great things about the PiSugar 3 that help here:  First, you can un-stick the battery from the board.  In fact, you can just go ahead and peel off the magnet from the battery and stick it on your fridge instead, because we ain't using it.

The other great thing about the PiSugar 3 is this header:

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54372078080/in/dateposted/" title="2025-02-23-223319-IMG_6031"><img src="https://live.staticflickr.com/65535/54372078080_c19a72d7ec_z.jpg" style="width:70%;max-width:512px;" alt="2025-02-23-223319-IMG_6031"/></a>

You know that [6-pin Molex Connector Cable, 1.25mm pitch](https://www.adafruit.com/product/4926) from the parts list?  It plugs right into that.  And you only need to connect four of the wires coming off it to the Raspberry Pi to get all the same functionality that you would if you installed the board the normal way.

Since we're on the subject of connectors, here are the accessories that come with the 10.3-inch e-paper display:

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54372078340/in/dateposted/" title="2025-02-17-163754-IMG_5997"><img src="https://live.staticflickr.com/65535/54372078340_0e89ac3fa7_z.jpg" style="width:70%;max-width:512px;" alt="2025-02-17-163754-IMG_5997"/></a>

See that connector cable near the top?  That plugs into the driver board included with the display, and can be used to connect the Raspbery Pi instead of piggybacking it on that giant GPIO header.

Here's a demonstration of this working, using a [mini black hat hack3r](https://shop.pimoroni.com/products/mini-black-hat-hack3r?variant=19448025991) board and some jumper wires:

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371682401/in/dateposted/" title="2025-02-17-192046-IMG_6005"><img src="https://live.staticflickr.com/65535/54371682401_3d5b2ed680_z.jpg" style="width:70%;max-width:512px;" alt="2025-02-17-192046-IMG_6005"/></a>

Now, a couple of the wires used by the e-paper driver board overlap with the PiSugar 3.  You're going to need three of those small crimp-on connectors to join them together when you wire everything up:

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371888739/in/dateposted/" title="2025-02-23-231851-IMG_6033"><img src="https://live.staticflickr.com/65535/54371888739_afec53a2a6_z.jpg" style="width:70%;max-width:512px;" alt="2025-02-23-231851-IMG_6033"/></a>

But this is honestly a small price to pay, to get rid of all those big ribbon cables, and eliminate any need to stack hardware.

Here's the configuration with the [mini black hat hack3r](https://shop.pimoroni.com/products/mini-black-hat-hack3r?variant=19448025991) factored out:

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54370809477/in/dateposted/" title="2025-02-24-075112-IMG_E6037"><img src="https://live.staticflickr.com/65535/54370809477_25fa7d513a_z.jpg" style="width:70%;max-width:512px;" alt="2025-02-24-075112-IMG_E6037"/></a>

This is the hardware as it will be assembled into the frame.

When the frame arrives from [Frame-It-Easy](https://www.frameiteasy.com/frame-styles/ashford?cid=1), it will be quite thoroughly packaged:

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54372077830/in/dateposted/" title="2025-03-05-203037-IMG_6085"><img src="https://live.staticflickr.com/65535/54372077830_2935ca1d05_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-05-203037-IMG_6085"/></a>

Separate the mat (the rectangular paper window that goes around the art) from the frame and lay it face down, and tape the display to the back of it.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54372078195/in/dateposted/" title="2025-03-05-211325-IMG_6091"><img src="https://live.staticflickr.com/65535/54372078195_54de53c549_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-05-211325-IMG_6091"/></a>

When I did this, I had the measurements slightly wrong: 8 1/2&quot; x 6 1/2&quot; instead of 8 3/4&quot; x 6 3/4&quot;, so I had to cut some material off the inside of the mat.  That's why mine looks a bit torn up.  Yours won't.  My pain is your gain!

Next, get the backing material out, because you're going to savage it with the x-acto knife:

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371682836/in/dateposted/" title="2025-03-05-211738-IMG_6092"><img src="https://live.staticflickr.com/65535/54371682836_8acf38015f_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-05-211738-IMG_6092"/></a>

Use a pencil to make marks in the shape of a slot, wide enough to fit the majority of the large ribbon cable through.  Cut from the underside -- it's a bit easier.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371918813/in/dateposted/" title="2025-03-05-203606-IMG_6088"><img src="https://live.staticflickr.com/65535/54371918813_ab169908c2_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-05-203606-IMG_6088"/></a>

At this point you're ready to assemble the frame.  Take my advice and make very sure that you wipe the dust off the display, the mat, and the plexiglass.  Dust is _sneaky!_

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371683071/in/dateposted/" title="2025-03-05-213209-IMG_6094"><img src="https://live.staticflickr.com/65535/54371683071_c756150cdc_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-05-213209-IMG_6094"/></a>

With a one-inch mat, there is enough space to pass the cable through without hitting the inside of the metal frame, and enough slack on the end to bend it around so it faces the other direction.

From there you can attach the little adaptor board, and then use some velcro to stick it to the backing.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54370809207/in/dateposted/" title="2025-03-06-174715-IMG_E6106"><img src="https://live.staticflickr.com/65535/54370809207_117527ca79_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-06-174715-IMG_E6106"/></a>

You could potentially assemble everything right now and just roll with it.  But if you do, you'll notice how much that connector on the driver board sticks out...

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371920798/in/dateposted/" title="2025-03-05-214029-IMG_6095"><img src="https://live.staticflickr.com/65535/54371920798_8ee6266d8a_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-05-214029-IMG_6095"/></a>

If you're feeling brave, now is the time to break out the Dremel tool and do something risky.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371920748/in/dateposted/" title="2025-03-06-164514-IMG_E6103"><img src="https://live.staticflickr.com/65535/54371920748_708448eb87_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-06-164514-IMG_E6103"/></a>

Put on some gloves and safety goggles.  Go outside and pour some water on the pavement.  This is so the metal bits will stick to it, until you can wipe them up with a few paper towels.

Then start carving!  Whooo!!

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54371920743/in/dateposted/" title="2025-03-06-165535-IMG_E6104"><img src="https://live.staticflickr.com/65535/54371920743_8654f3241f_z.jpg" style="width:70%;max-width:512px;" alt="2025-03-06-165535-IMG_E6104"/></a>

This socket sticks up a lot, and you don't need it at all.  Carve that sucker down.  Chop the pins off the connector on the other side too, if you feel like it.

One more thing for saving space:  You only need to attach twelve wires to twelve pins on the Raspberry Pi.  Feel free to bend them down.

<a data-flickr-embed="true" href="https://www.flickr.com/photos/57897385@N07/54372076420/in/dateposted/" title="2025-02-25-233332-IMG_6044"><img src="https://live.staticflickr.com/65535/54372076420_74c7bc4d5d_z.jpg" style="width:70%;max-width:512px;" alt="2025-02-25-233332-IMG_6044"/></a>

And that's all it takes to assemble this project.

### Wiring





# Software

