# heavily inspired by https://www.nodebox.net/code/index.php/Landslide

from __future__ import print_function

import sys, os

import pprint
pp = pprint.pprint
kwdbg = 0
kwlog = 0

# need a different name for nodebox
import random as rnd

import libgradient

if kwdbg and 1:
    # make random choices repeatable for debugging
    rnd.seed( 123456 )


# width and height of destination image
# W, H =  800,  600
# W, H = 1024,  768
# W, H = 1280,  800
# W, H = 1440,  900
W, H = 1920, 1080

# import photobot lib
try:
    pb = ximport("photobot")
    size(W, H)
    background( 0.333 )
except ImportError:
    pb = ximport("__init__")
    reload(pb)
    size(W, H)
    background( 0.333 )
except NameError:
    import photobot as pb
    WIDTH, HEIGHT = W, H
    print( "File: %s" % (__file__,) )
RATIO = WIDTH / HEIGHT

# load the image library
# check for command line folders
additionals = sys.argv[1:]

# get all images from user image wells
imagewell = pb.loadImageWell(   bgsize=(WIDTH, HEIGHT),
                                minsize=(256,256),
                                pathonly=True,
                                additionals=additionals,
                                resultfile="imagewell-files",
                                ignoreFolderNames=('+offline',))

# tiles are images >256x256 and <=WIDTH, HEIGHT
tiles = imagewell['tiles']

# backgrounds are images >W,H
backgrounds = imagewell['backgrounds']

print( "tiles: %i" % len(tiles) )
print( "backgrounds: %i" % len(backgrounds) )


# create the canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (85,85,85) )


if not kwdbg:
    turns = int( round(20 + (rnd.random() * 10)) )
    if kwlog:
        print( "shuffle turns: %i" % turns )
    for turn in range( turns ):
        rnd.shuffle(tiles)
        rnd.shuffle(backgrounds)


def grid(cols, rows, colSize=1, rowSize=1, shuffled=False):
    """Returns an iterator that contains coordinate tuples.
    Taken from nodebox.utils
    """
    rowRange = list(range(int(rows)))
    colRange = list(range(int(cols)))
    # Shuffled needs a real list, though.
    if (shuffled):
        rnd.shuffle(rowRange)
        rnd.shuffle(colRange)
    for y in rowRange:
        for x in colRange:
            yield (x*colSize,y*rowSize)



# CONFIGURATION

columns = 9
rows = 4

colwidth = int(WIDTH / columns)
rowheight = int(HEIGHT / rows)
maxsize = int(max(colwidth,rowheight)*1.2)
maxsize = int( rowheight * 1.2 )

# print "colwidth/rowheight:", colwidth, rowheight

xgutter = colwidth * 0.0667
ygutter = rowheight * 0.0667
# print "xgutter/ygutter:", xgutter, ygutter

realwidth = colwidth - 1*xgutter
realheight = rowheight - 1*ygutter 

positions = list(grid(columns, rows, colwidth, rowheight, shuffled=True))

randomblur = not kwdbg
paintoverlay = 0 # not kwdbg
gilb = 0

#
# Base Image
#

#  create, scale and place the image
x, y = 0, 0
bgimage = backgrounds.pop()
top, w, h = pb.placeImage(c, bgimage, x, y, W, "Image 1")
print( "Background: %s" % bgimage.encode("utf-8") )

for position in positions:
    x, y = position

    # create image in canvas at 0,0
    p = tiles.pop()
    print(p.encode("utf-8"))
    top, w, h = pb.placeImage(c, p, 0, 0, maxsize=None, name="Image %i,%i" % (x,y)) #, width=False, height=True)

    # scale the layer to row height
    if rnd.random() > 0.5:
        # random row height 0.5 <= x <= 4.5
        tileheight = rowheight * (0.5 + rnd.random() * 3.0)
    else:
        # random row height is integer multiple
        tileheight = rowheight * rnd.choice( (1,2,3,4,5) )
    pb.scaleLayerToHeight( c.top, tileheight )

    # uniform width
    #layer = cropImageToRatioHorizontal( layer, RATIO )

    # get the new image bounds
    w, h = c.top.bounds()
    halfwidth = int(w/2.0)

    # add contrast
    c.top.contrast(1.1)

    r = rnd.random()
    # 10%
    if 0 < r < 0.2:
        #print "20% LINEAR"
        # create gradient layer
        # top is now gradient index
        top = c.gradient(pb.LINEAR, halfwidth, h)
        c.top.flip( pb.HORIZONTAL )

        # layer + 4 flip
        # c.top.flip( pb.HORIZONTAL )

        # layer +4 translate half a pict right
        c.top.translate(halfwidth, 0)

        # create gradient layer
        # top is now second gradient index
        top = c.gradient(pb.LINEAR, halfwidth, h)

        # merge both gradients; destroys top layer
        c.merge([ top-1 , top ])
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
        radius = int( w / 5.0 )
        top = c.gradient(pb.ROUNDRECT, w, h, "", radius=radius, radius2=radius)
    elif r >= 0.8:
        #print "20% QUAD"
        top = c.gradient(pb.QUAD, w, h, "", 0, 0)
            
    # print "After mask"
    c.top.brightness(1.4)

    # mask destroys top layer
    c.top.mask()

    destx = x - xgutter
    desty = y - ygutter
    c.top.translate(x, y)
    
    c.top.opacity( 50 + rnd.random() * 50 )

    if randomblur:
        if rnd.random() > 0.75:
            #print "FLIP"
            c.top.flip()

        if rnd.random() > 0.75:
            #print "BLUR"
            c.top.blur()
    
    if randomblur:
        if rnd.random() > 0.75:
            c.top.flip()

        if rnd.random() > 0.75:
            c.top.blur()

    if rnd.random() > 0.9:
        print("BLEND SCREEN")
        c.top.screen()

    if rnd.random() > 0.9:
        print("BLEND COLOR")
        c.top.color()

if gilb:
    # orange hue overlay finish
    # create new color layer
    if kwlog and 1:
        print("Orange gilb start")
    c.flatten()
    c.fill((200,100,0))
    c.top.opacity(30)
    c.top.hue()
    if kwlog and 1:
        print("Orange gilb end")


paintfile = os.path.abspath("./paint.jpg")
if paintoverlay:
    # paint overlay
    if os.path.exists( paintfile ):
        if kwdbg or 1:
            print( "paint overlay start")
        c.flatten()
        topidx = c.layer( paintfile )
        w, h = c.top.bounds()
        xs = WIDTH / float(w)
        ys = HEIGHT / float(h)
        s = max(xs,ys)
        c.top.scale(s, s)
        c.top.opacity( 90 )
        c.top.overlay()
        if kwdbg or 1:
            print( "paint overlay end")

c.draw(0,0)


