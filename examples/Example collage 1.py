

# heavily inspired by https://www.nodebox.net/code/index.php/Landslide

from __future__ import print_function

import sys, os

import pprint
pp = pprint.pprint
kwdbg = 0

# need a different name for nodebox
import random as rnd

import libgradient

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

# width and height of destination image
W, H =  800,  600
W, H = 1024,  768
W, H = 1280,  800
W, H = 1440,  900
W, H = 1920, 1080

# import photobot
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
RATIO = WIDTH / HEIGHT

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

# backgrounds are images >W,H
backgrounds = imagewell['backgrounds']

rnd.shuffle(tiles)
rnd.shuffle(backgrounds)

print( "tiles: %i" % len(tiles) )
print( "backgrounds: %i" % len(backgrounds) )


# create the canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (85,85,85) )


# CONFIGURATION

columns = 3
rows = 3

enoughTiles = len(tiles) > (columns * 2 * rows)

randomblur = 1
randomflip = 1
paintoverlay = 1
gilb = 1


# 
y_offset = HEIGHT / float(rows)
y_offset = int(round(y_offset))




# background image
bgimage = backgrounds.pop()
pb.placeImage(c, bgimage, 0, 0, WIDTH, "Image 1")
# print( "Background: %s" % bgimage.encode("utf-8") )


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

        # get current image bounds
        w, h = c.top.bounds()

        
        # calculate scale & apply
        s = pb.aspectRatio( (w,h), y_offset, height=True)
        c.top.scale(s, s)

        # get current image bounds
        w, h = c.top.bounds()

        # create a random mask gradient for this tile
        libgradient.makerandomgradient( c, w, h, j*y_offset )
        c.top.mask()


        # P: 0.5 # flip the tile
        if randomblur:
            if rnd.random() > 0.5:
                c.top.flip()

        # P: 0.5 # add blur
        if randomflip:
            if rnd.random() > 0.5:
                c.top.blur()

        w, h = c.top.bounds()
        c.top.translate(colw, j*y_offset)
        colw += w


if 1:
    # orange hue mask finish
    topidx = c.fill((200,100,0))
    c.top.opacity(30)
    c.top.hue()

paintfile = os.path.abspath("./paint.jpg")
if paintoverlay:
    # paint overlay
    if os.path.exists( paintfile ):
        if kwdbg:
            print( "paint overlay:  %s" % paintfile )
        topidx = c.layer( paintfile )
        w, h = c.top.bounds()
        xs = WIDTH / float(w)
        ys = HEIGHT / float(h)
        s = max(xs,ys)
        c.top.scale(s, s)
        # c.top.opacity( 90 )
        c.top.overlay()

c.draw(0,0)

