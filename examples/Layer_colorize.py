import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

W, H = 532, 1050


# check for Nodebox
NB = True
try:
    _ctx
except(NameError):
    NB = False

if NB:
    size(W, H)
    pb = ximport("photobot")
else:
    WIDTH, HEIGHT = W, H
    import photobot as pb


if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

imagewell = pb.loadImageWell()
tiles = imagewell['backgrounds']
rnd.shuffle(tiles)


# pick 2 images
img1path = tiles.pop()
img2path = tiles.pop()

# create a white canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (192, 192, 192) )

#
# Image 1
#

print( img1path.encode("utf-8") )
#  create, scale and place the image
x, y = 10, 10
top, w1, h1 = pb.placeImage(c, img1path, x, y, 512, "Image 1")
pb.label(c, "Image 1", x, y, 30)

x, y = 10, h1 + 10 + 10
top, w1, h1 = pb.placeImage(c, img1path, x, y, 512, "Image 1 colored")

# apply colorize

# c.top.colorize((192, 120, 0), (240, 255, 127))

c.top.colorize( black=( 60,  60, 0),
                white=(250, 200, 96),
                  mid=(220, 190, 16))

pb.label(c, "Image 1 colored", x, y, 30)


# draw the result
c.draw(0, 0)
