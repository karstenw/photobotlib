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


# CONFIGURATION

columns = 3
rows = 3

enoughTiles = len(tiles) > (columns * 2 * rows)

randomblur = 1
randomflip = 1
paintoverlay = 0
gilb = 0


# 
y_offset = HEIGHT / float(rows)
y_offset = int(round(y_offset))

# background image
bgimage = backgrounds.pop()
pb.placeImage(c, bgimage, 0, 0, WIDTH, "Image 1")
print( "Background: %s" % bgimage.encode("utf-8") )

tilecounter = 0
cols = -1
for j in range(rows):
    colw = 0
    cols += 1
    while colw < WIDTH:

        # create image in canvas at 0,0
        nextpictpath = tiles.pop()

        # new layer with a random image
        # c.layer returns the index of the top layer
        topidx = c.layer( nextpictpath )
        tilecounter += 1
        if kwlog or 1:
            print( "%i  -- %s" % (tilecounter, nextpictpath.encode("utf-8")) )

        # get current image bounds
        w, h = c.top.bounds()

        # calculate scale & apply
        s = pb.aspectRatio( (w,h), y_offset, height=True)
        c.top.scale(s, s)
        if kwlog:
            print( "Scale" )

        # get current image bounds
        w, h = c.top.bounds()

        # create a random mask gradient for this tile
        if kwlog:
            print( "Gradient" )
        libgradient.makerandomgradient( c, w, h, j*y_offset )
        if kwlog:
            print( "Mask" )
        c.top.mask()


        # P: 0.5 # flip the tile
        if randomblur:
            if rnd.random() > 0.5:
                if kwlog or 1:
                    print( "Flip" )
                c.top.flip()

        # P: 0.5 # add blur
        if randomflip:
            if rnd.random() > 0.5:
                if kwlog or 1:
                    print( "Blur" )
                c.top.blur()

        w, h = c.top.bounds()
        if kwlog:
            print( "Translate" )
        c.top.translate(colw, j*y_offset)
        colw += w

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


