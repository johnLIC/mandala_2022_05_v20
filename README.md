# mandala_2022_05_v20
mandala code from imgur

This is an example of code I use to make little 3 second animations that look like loading icons or mandalas.  There are 5 flags that should be passed when 
running this script from a command line:
<start frame> <end frame> <show image?> <save file?> <make gif?>
  
SO, if you just want to see the first frame of myfile.py:
  
python myfile.py 0 1 1 0 0
  
If you want to run a whole 90 frame sequence:

python myfile.py 0 90 0 1 1 
  
The <end frame> is "strictly less than" because it is being passed to a range() function, so you'd get frames 0 through 89 in the above example.
  
I am running this on Win 10 on a Acer Nitro 5 laptop.  I used to run on a linux machine with 16 cores, and there is some commented out code that did multi-threading.  It
won't just turn on and work, though. I had to change a couple things to get it to work without the multithreading.  
  
The equations that do the drawing are just the result of my endless nudging on the numbers to make things that are visually interesting to me.  There's no rhyme or reason
to them - no theoretical underpinning or famous math ideas being explored, it's just me screwing around with sin and cos.
  
I'm sorry this code is such a mess.  It was not written to be shared, so good luck. :)
