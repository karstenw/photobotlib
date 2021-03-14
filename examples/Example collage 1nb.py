

# heavily inspired by https://www.nodebox.net/code/index.php/Landslide

from __future__ import print_function

import sys, os

import pprint
pp = pprint.pprint
kwdbg = False

# need a different name
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)


W, H = 1024,768
W, H = 1920, 1050


# check for Nodebox
NB = True
try:
    _ctx
except(NameError):
    NB = False

if NB:
    size(W, H)
    pb = ximport("photobot")
    background( 0.333 )
else:
    WIDTH, HEIGHT = W, H
    import photobot as pb

RATIO = WIDTH / HEIGHT

# load the image library
# check for command line folders
additionals = sys.argv[1:]

# get all images from user image wells
imagewell = pb.loadImageWell(   bgsize=(WIDTH, HEIGHT),
                                minsize=(256,256),
                                pathonly=True,
                                additionals=additionals)

# tiles are images >256x256 and <=1024x768
tiles = imagewell['tiles']

# backgrounds are images >1024x768
backgrounds = imagewell['backgrounds']
rnd.shuffle(tiles)
rnd.shuffle(backgrounds)

print( "tiles: %i " % len(tiles) )
print( "backgrounds: %i" % len(backgrounds) )


# CONFIGURATION

# create the canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (85,85,85) )


# CONFIGURATION

columns = 5
rows = 3

randomblur = 0
randomflip = 0
paintoverlay = 0
gilb =0


# 
y_offset = HEIGHT / float(rows)
y_offset = int(round(y_offset))

x_offset = WIDTH / float(columns)

# 
if 0:
    bgimage = backgrounds.pop()
    top = c.layer(bgimage)
    w, h = c.top.bounds()
    w1,h1 = pb.aspectRatio( (w,h), WIDTH, height=False, assize=True )
    c.top.scale(w1,h1)
else:
    bgimage = backgrounds.pop()
    pb.placeImage(c, bgimage, 0, 0, WIDTH, "bgimage")
print( "Background:  %s" % bgimage.encode("utf-8") )

idx = 0

for j in range(rows):
    colw = 0
    for i in range(columns):
        idx += 1
        # new layer with a random image
        top = c.layer( tiles.pop() )

        # get current image bounds
        w, h = c.top.bounds()

        # calculate scale & apply
        s = pb.aspectRatio( (w,h), y_offset, height=True)
        c.top.scale(s, s)

        # uniform
        layer = pb.cropImageToRatioHorizontal( c.top, RATIO )

        # add contrast
        c.top.contrast(1.1)

        # get the new image bounds
        w, h = c.top.bounds()

        r = 0.4 
        r = rnd.random()
        # 10%
        if r < 0.1:
            # create a dual ramp gradient
            _ = c.gradient(pb.LINEAR, w/2, h)
            c.top.flip( pb.HORIZONTAL )

            # layer translate half a pict right
            c.top.translate(w/2, j*y_offset)

            # create another gradient layer and merge with first gradient
            top = c.gradient(pb.LINEAR, w/2, h)
            # merge both gradients; destroys top layer
            c.merge([ top-1 , top ])
        elif 0.1 <= r < 0.5:
            # SINE
            top = c.gradient(pb.SINE, w, h)
            
        elif 0.6 <= r < 0.75:
            # RADIALCOSINE
            top = c.gradient(pb.RADIALCOSINE, w, h)
            c.top.invert()
        else:
            # ROUNDRECT
            # 25%
            top = c.gradient(pb.ROUNDRECT, w, h, radius=int(w/5.0))

        c.top.brightness(1.4)

        # mask destroys top layer
        c.top.mask()
        
        # c.top.translate(colw+i*w, j*y_offset)
        c.top.translate(x_offset * i, j*y_offset)
        
        c.top.opacity( 66 + rnd.random() * 29 )

        if randomblur:
            if rnd.random() > 0.5:
                c.top.flip()

            if rnd.random() > 0.5:
                c.top.blur()

if 1:
    # orange hue mask finish
    top = c.fill((200,100,0))
    c.top.opacity(30)
    c.top.hue()

if paintoverlay:
    # paint overlay
    top = c.layer( os.path.abspath("./paint.jpg") )
    w, h = c.top.bounds()
    xs = WIDTH / float(w)
    ys = HEIGHT / float(h)
    s = max(xs,ys)
    c.top.scale(s, s)
    c.top.opacity(10)
    c.top.overlay()

c.draw(0, 0)
