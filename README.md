<bold>dmxSnake Readme</bold>
Thanks for checking out dmxSnake! I'm a board op not a software engineer, so I'm aware this code is messy and performing sub optimal math in a lot of places, but it's good enough to hit 40fps on a Raspberry Pi so it's good enough for github. If you feel like optimizing or improving, be my guest.
<bold>Setup</bold>
This script requires Python (and pyGame, which normally comes with it) as well as OLA to handle the dmx output. OLA works on Mac and Linux, if you have Windows, spin up a virtual Linux box.
https://www.openlighting.org/ola/getting-started/downloads/
Once OLA is installed, it will begin serving a webpage at yourip:9090 . You can use this page to configure OLA. To begin, click add universe. Here you can set the number of the universe just like a console and label it. After that, select the type of protocol you'd like to use. This will probably be ArtNet or E1.31(sACN) but you can also output to a physical dmx dongle if you have that configured. Click add universe.
OLA is now set up to start sending data over your preferred protocol to your transmitter.
<bold>Settings in the Script</bold>
Before you run the script for the first time, you need to edit the variable "universe" on line 58 to reflect the universe you just configured in OLA. It defaults to 2 because that's what I was using for testing.
While you're in the script you can also change the size of your pixel array with the "pxlWidth" and "pxlHeight" on lines 54 and 55. I've started an 8x8 grid with a box of Helios in mode 42 in mind as the default setup, but the game should scale to any array with 170 pixels or less(width*height) (1 universe of dmx).
You can also adjust the speed of your snake and therefore difficulty with the "velocity" variable on line 44.
You can add custom colors by adding new variables under line 21. These should be r,g,b values from 0-255. AKA your color from the console.
Once you've added colors or not, you can choose which colors are applied to which objects when we build the dmx packet from line 200-225. There are 3 types of objects, 1 is the snake head, 2 is the snake tail, and 3 is food. You can set the colors by changing what dmx color they reference in this section. By default the snake and its tail are teal and food is pink, but you can set the head or tail to another color to improve visability if you wish.
<bold>Playing the Game</bold>
After configuring you can run the script. A window with the game's menu will appear and the script will start outputting [0,0,0] (black) to every dmx pixel. Once it's running you can press space to start the game. When you die you can also mash(you have to mash to get the correct timing cause my code sucks) space to restart and try again.
The arrow keys control movement and the numbers control the intensity of your lights with 1 being 10% and 0 being full.

That's about it. If you have any questions feel free to dm me. Have fun playing! 
