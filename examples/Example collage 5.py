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

xgutter = colwidth * 0.0667
ygutter = rowheight * 0.0667

realwidth = colwidth - 1*xgutter
realheight = rowheight - 1*ygutter 

positions = list(grid(columns, rows, colwidth, rowheight, shuffled=True))
# positions.extend( list(grid(columns, rows, colwidth, rowheight, shuffled=True)) )
# positions.extend( list(grid(columns, rows, colwidth, rowheight, shuffled=True)) )

randomblur = 0 # not kwdbg
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
    top, w, h = pb.placeImage(c, p, 0, 0, maxsize=None, name="Image %i,%i" % (x,y))


    # scale the layer to row height
    if rnd.random() > 0.5:
        # random row height 0.5 <= x <= 4.5
        tileheight = rowheight * (0.5 + rnd.random() * (rows-1))
    else:
        # random row height is integer multiple
        choices = range( 1, rows+1 ) # (1,2,3,4,5)
        tileheight = rowheight * rnd.choice( choices )
    pb.scaleLayerToHeight( c.top, tileheight )

    # get the new image bounds
    w, h = c.top.bounds()
    halfwidth = int( w / 2.0 )

    
    # add contrast
    c.top.contrast(1.1)


    if kwdbg:
        print("LINEAR")

    # create up and downramp mask
    top = c.gradient(pb.LINEAR, halfwidth, h)
    c.top.flip( pb.HORIZONTAL )
    c.top.translate(halfwidth, 0)
    top = c.gradient(pb.LINEAR, halfwidth, h)
    c.merge([ top-1 , top ])

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


