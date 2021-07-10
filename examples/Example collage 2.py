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

columns = 8
rows = 4

# 
y_offset = HEIGHT / float(rows)
y_offset = int(round(y_offset))

enoughTiles = len(tiles) > (columns * 2 * rows)

randomblur = 0
randomflip = 0
paintoverlay = 0
gilb = 0

picts = []
for t in range(columns*rows*2):
    s = rnd.choice(tiles)
    picts.append(s)
    if 0: #enoughTiles:
        tiles.remove(s)
# rnd.shuffle(picts)

# background image
bgimage = backgrounds.pop()
pb.placeImage(c, bgimage, 0, 0, WIDTH, "bgimage")
print( "Background: %s" % bgimage.encode("utf-8") )


tilecounter = 0
for j in range(rows):
    for i in range(columns):

        # create image in canvas at 0,0
        nextpictpath = picts.pop()
        c.layer( nextpictpath )
        tilecounter += 1
        if kwdbg or 1:
            print( "%i  -- %s" % (tilecounter, nextpictpath.encode("utf-8")) )

        # add contrast
        c.top.contrast(1.1)

        # get current image bounds
        w, h = c.top.bounds()
        halfwidth = int( w / 2.0 )


        if kwdbg:
            print( "Gradient 1" )

        # create gradient layer
        c.gradient(pb.LINEAR, int(w/2), h)

        if kwdbg:
            print( "Gradient 1 flip" )

        # layer + 4 flip
        c.top.flip()

        if kwdbg:
            print( "Gradient 1 translate" )

        # layer +4 translate half a pict right
        c.top.translate(w/2, j*y_offset)

        if kwdbg:
            print( "Gradient 2" )

        # create gradient layer
        c.gradient(pb.LINEAR, int(w/2), h)

        if kwdbg:
            print( "Gradient 2 merge with gradient 1" )

        # merge the 2 gradient ramps
        top = c.topindex
        c.merge([top-1, top])

        if kwdbg:
            print( "Gradient brightness 1.4" )

        c.top.brightness(1.4)

        if kwdbg:
            print( "Gradient mask" )

        c.top.mask()
        c.top.translate(i*w/3, j*y_offset)


        if kwdbg:
            print( "Layer flip" )

        if rnd.random() > 0.5:
            if kwdbg:
                print( "flip" )
            c.top.flip()

        if kwdbg:
            print( "Layer blur" )

        if rnd.random() > 0.5:
            if kwdbg:
                print( "blur" )
            c.top.blur()

        if kwdbg:
            print( "Layer merge with previous" )


        # merge with previous layer fro memory reasons
        top = c.topindex
        if top > 2:
            c.merge([top-1, top])



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


