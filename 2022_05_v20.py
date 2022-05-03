#!C:\Users\yesth\anaconda3\python.exe


# multi-threaded animated mandala (or random image) maker.
# ./multi_v03.py 90 0 1

#  args:
#  1) start frame, sys.argv[0]
#  2) end frame, sys.argv[1]
#  3) flag to display sys.argv[2]
#  4) flag to render sys.argv[3]
#  5) sys.argv[3] make animated gif 0/1

# to make images
from PIL import Image
import math
from math import sin,cos,radians,e,sqrt,pow
import random
import sys
import os
import subprocess

# for multiprocessing
from functools import partial
import time
import multiprocessing
 

#####################################################


# the multiprocessing version of this seems very picky about data types.
def pixelCalc(t):
    pitch = .005
    x = (180-.25*t)*sin(t + sin(radians(4*frame))) + (20 - .08*t+20*sin(radians(8*frame)))*(sin(10*t + .008*pow(t,.25))) + (12 +.19*t+20*sin(2*radians(4*frame)))*sin(6*t -.08*t)
    y = (180-.25*t)*cos(t + sin(radians(4*frame))) + (20 - .08*t+20*sin(radians(8*frame)))*(cos(10*t + .008*pow(t,.25))) + (12 +.19*t+20*sin(2*radians(4*frame)))*cos(6*t -.08*t)
    
    dt = t+.006
    dx = (120-.05*dt)*sin(dt + sin(radians(4*frame))) + (20 - .08*dt+40*sin(radians(4*frame)))*(sin(4*dt + .003*pow(dt,.5))) + (12 +.19*dt+18*sin(radians(8*frame)))*sin(6*t -.008*dt)
    dy = (120-.05*dt)*cos(dt + sin(radians(4*frame))) + (20 - .08*dt+40*sin(radians(4*frame)))*(cos(4*dt + .003*pow(dt,.5))) + (12 +.19*dt+18*sin(radians(8*frame)))*cos(6*t -.008*dt)
    mag = ((x-dx)*(x-dx) + (y-dy)*(y-dy)) / math.sqrt((x*x + y*y))
    
    t2 = t + 2*math.pi + cos(radians(frame*4))
    x2 = (220-.25*t2)*sin(t2 + .4*sin(radians(4*frame))) + (20 - .18*t2+80*sin(radians(4*frame)))*(sin(5*t2 + .003*pow(t2,.5))) + (12 +.19*t2+8*sin(radians(4*frame)))*sin(6*t2 -.008*mag)
    y2 = (220-.25*t2)*cos(t2 + .4*sin(radians(4*frame))) + (20 - .18*t2+80*sin(radians(4*frame)))*(cos(5*t2 + .003*pow(t2,.5))) + (12 +.19*t2+8*sin(radians(4*frame)))*cos(6*t2 -.008*mag)

    
    x = math.pow((.000005 + 8*pitch*t), 1.05)*x + W*.5
    y = math.pow((.000005 + 8*pitch*t), 1.05)*y + H*.5
    #print x,y    
    x2 = math.pow((.000005 + 8*pitch*t), 1.06)*x2 + W*.5
    y2 = math.pow((.000005 + 8*pitch*t), 1.06)*y2 + H*.5

    return [ int(x), int(y) ], mag, [int(x2), int(y2)]  # return one pixel's color data tuple

# This gets called by the pool - each process does one row.
def imageMaker(t_range):
    revolutions = 2
    arc_length = .001
    t = 0.0 #t_range*2*math.pi*revolutions
    while t < (t_range+1)*2*math.pi*revolutions -1.55:
        pixel = (pixelCalc(t))
        #print("pixel %s = %s" %(t,pixel))
        t = t + arc_length
        #if pixel[0][0] < W-1 and pixel[0][0] > 0 and pixel[0][1] < H-1 and pixel[0][1] > 0:
        #    RGB[pixel[0][0]*W + pixel[0][1]] = (int(255-10000*pixel[1]*pixel[1]*(2+sin(radians(frame*4)))), 255 - int(.5*max(0,min(255,300000000*pixel[1]))), int(max(0,min(255,200000000000*pixel[1]))))
        bands = 20  # 800
        for i in range(bands):
            exp = 1+.1*(i/bands)*sin(radians(frame*4))
            x_fade = (pow((float(i)/bands),exp) * pixel[0][0] + pow((1.0 - float(i)/bands),exp)* pixel[2][0] )
            y_fade = (pow((float(i)/bands),exp) * pixel[0][1] + pow((1.0 - float(i)/bands),exp)* pixel[2][1] )
            if x_fade < W-1 and x_fade > 0 and y_fade < H-1 and y_fade > 0:
                #RGB[x_fade*W + y_fade] = (int(255-(float(i)/5.0)*10000*pixel[1]*pixel[1]*(2+sin(radians(frame*4)))), 255 - int(.5*max(0,min(255,300000000*pixel[1]))), int(max(0,min(255,(1.0 - float(i)/5.0)*200000000000*pixel[1]))))
                RGB[int(x_fade)*W + int(y_fade)] = (int(255-(float(i)/3000.0)*.2*pixel[1]*pixel[1]*(20+sin(radians(frame*8)))), int((float(i)/float(bands))*min(255,160*(1.0 + cos(radians(6*pixel[1]))))), int(max(0,min(255,(1.0 - float(i)/bands)*100*pixel[1]))))
                #print("RGB=%s" % RGB[int(x_fade)*W + int(y_fade)])
    return RGB

        


# After the pool happens, put the data into an image format, and save and/or gificate the images
def image_array_munger(show, save, gif):
    #print "array munger"
    #print "len(RGB)=", len(RGB)
    RGB_flat = []
    for chunk in RGB:
        #print("chunk = ")
        #print(chunk)
        for elem in chunk:
            #print(elem)
            RGB_flat.append(elem)
    #print( "len RGB_flat= ", len(RGB_flat))
    im = Image.new("RGB", (W,H))
    RGB_tuple = (RGB[0])
    im.putdata(RGB)
    if show==1:
        #print "showing frame " + str(frame)
        im.show()
    if save==1:
        print("saving " + str(frame))
        #print('render/'+sys.argv[0].split(".")[1] + "/" + sys.argv[0].split(".")[1] + "." + str(frame).zfill(4) + '.png')
        #if not os.path.exists('render/'+sys.argv[0].split(".")[1] ):
        #    os.makedirs('render/'+sys.argv[0].split(".")[1] )
        #im.save('render/'+sys.argv[0].split(".")[1] + "/" + sys.argv[0].split(".")[1] + "." + str(frame).zfill(4) + '.png')
        if not os.path.exists(sys.argv[0].split(".")[0] + "/render/" ):
            os.makedirs(sys.argv[0].split(".")[0] + "/render/" )
        im.save(sys.argv[0].split(".")[0] + "/render/" + sys.argv[0].split("\\")[-1].split(".")[0] + "." + str(frame).zfill(4) + '.png')


#####################################################

frame_start = int(sys.argv[1])
frame_end = int(sys.argv[2])
W=1000
H=1000

if __name__=='__main__':

    for frame in range(frame_start, frame_end):
        RGB = [(0,0,0)]*W*H  # I don't remember why we want RGB in array_munger
        #print len(RGB)
        #pool = multiprocessing.Pool(processes=10)  # run this many processes, so we don't double-write into RGB
        #RGB = pool.map(imageMaker, range(0,10))  # run one process for each row in the image
        #pool.close()  # "we are not adding any more threads" 
        #pool.join()  # wait for all the threads, or maybe that's what the next line does.
        #print "size RGB = " + str(len(RGB))
        #print RGB[0]
        imageMaker(10)
        image_array_munger(int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))  # assemble image data array, argv[2] = show?, argv[3] = save?

    # make an animated gif
    if sys.argv[5] == "1":            
        input_path = sys.argv[0].split(".")[0]+"/render/"+sys.argv[0].split("\\")[-1].split(".")[0] + ".%4d.png"         
        if not os.path.exists(sys.argv[0].split(".")[0] + "/gif/"):
            os.makedirs(sys.argv[0].split(".")[0] + "/gif/")
        output_path = sys.argv[0].split(".")[0] + "/gif/" + sys.argv[0].split("\\")[-1].split(".")[0] + '.gif'
        subprocess.check_call(["attrib", "-r", sys.argv[0].split(".")[0] + "/gif/"])
        print("output path %s" % output_path)
        #  convert -delay 10 -loop 0 render/v08.*.png gif/v002_02.gif
        os.system("ffmpeg -i " + input_path + " " + output_path)

       
