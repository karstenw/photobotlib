# heavily inspired by https://www.nodebox.net/code/index.php/Landslide

import sys
import os

W,H = 1920, 1080
RATIO = W / H

kwdbg = False

size(W, H)

background( 0.333 )

# need a different name; random is taken
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

# import photobot
try:
    pb = ximport("photobot")
    pbh = ximport("pbhelpers")
except ImportError:
    pb = ximport("__init__")
    reload(pb)

# from pbhelpers import *


# create the canvas
c = pb.canvas(int(WIDTH), int(HEIGHT))

# load the image library
# check for command line folders
additionals = sys.argv[1:]

# get all images from user image wells
imagewell = pb.loadImageWell(   bgsize=(W,H),
                                minsize=(256,256),
                                pathonly=True,
                                additionals=additionals)

# tiles are images >256x256 and <=1024x768
tiles = imagewell['tiles']

# backgrounds are images >1024x768
backgrounds = imagewell['backgrounds']
rnd.shuffle(tiles)
rnd.shuffle(backgrounds)

print "tiles:", len(tiles)
print "backgrounds:", len(backgrounds)


bgimage = backgrounds.pop()


# CONFIGURATION
columns = 5
rows = 3

colwidth = int(WIDTH / columns)
rowheight = int(HEIGHT / rows)
maxsize = int(max(colwidth,rowheight)*1.2)

# print "colwidth/rowheight:", colwidth, rowheight

xgutter = colwidth * 0.0667
ygutter = rowheight * 0.0667
# print "xgutter/ygutter:", xgutter, ygutter

realwidth = colwidth - 1*xgutter
realheight = rowheight - 1*ygutter 

positions = list(grid(columns, rows, colwidth, rowheight))

randomblur = not kwdbg
paintoverlay = not kwdbg


#
# Base Image
#

#  create, scale and place the image
x, y = 0, 0
top, w, h = pb.placeImage(c, bgimage, x, y, W, "Image 1")


for position in positions:
    x, y = position


    # create image in canvas at 0,0
    p = tiles.pop()
    print p
    top, w, h = pb.placeImage(c, p, 0, 0, maxsize, "Image %i,%i" % (x,y))

    # scale the layer to row height
    pb.scaleLayerToHeight( c.top, rowheight )

    # uniform width
    #cropImageToRatioHorizontal( c.top, RATIO )

    # get the new image bounds - layer still valid
    w, h = c.top.bounds()

    # add contrast - layer still valid
    c.top.contrast(1.1)


    r = rnd.random()
    # 10%
    if 0 < r < 0.2:
        #print "20% LINEAR"
        # create gradient layer
        # top is now gradient index
        c.gradient(pb.LINEAR, int(w/2), h)
        c.top.flip( pb.HORIZONTAL )

        # translate half a pict right
        c.top.translate(w/2, 0)

        # create gradient layer
        # top is now second gradient image
        topidx = c.gradient(pb.LINEAR, int(w/2), h)

        # merge both gradients; destroys top layer
        c.merge([ topidx-1 , topidx ])

    elif 0.2 <= r < 0.4:
        #print "20% SINE"
        top = c.gradient(pb.SINE, w, h)
        
    elif 0.4 <= r < 0.6:
        #print "20% RADIALCOSINE"
        top = c.gradient(pb.RADIALCOSINE, w, h)
        # c.top.invert()
    elif 0.6 <= r < 0.8:
        #print "20% ROUNDRECT"
        # 25%
        top = c.gradient(pb.ROUNDRECT, w, h, "", radius=w/5.0, radius2=w/5.0)
    elif r >= 0.8:
        #print "20% QUAD"
        top = c.gradient(pb.QUAD, w, h, "", 0, 0)
            
    # enhance mask
    c.top.brightness(1.4)
    c.top.mask()

    # top layer is now image with mask

    destx = x - xgutter
    desty = y - ygutter
    # print "Image@", x, y
    # c.top.translate(destx, desty)
    c.top.translate(x, y)

    if randomblur:
        if rnd.random() > 0.75:
            #print "FLIP"
            c.top.flip()

        if rnd.random() > 0.75:
            #print "BLUR"
            c.top.blur()

if 0:
    # orange hue mask finish
    #print "Mr. Orange"
    top = c.fill((200,100,0))
    c.top.opacity(30)
    c.top.hue()

if paintoverlay:
    # paint overlay
    #print "VINCENT"
    top = c.layer( os.path.abspath("./paint.jpg") )
    w, h = c.top.bounds()
    xs = WIDTH / float(w)
    ys = HEIGHT / float(h)
    s = max(xs,ys)
    c.top.scale(s, s)
    c.top.opacity(50)
    c.top.overlay()

c.draw(0, 0)
