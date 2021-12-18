import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

W, H = 542, 1050
fullwidth = int(W-20)
tilewidth = int((fullwidth-10) / 2.0)


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

import imagewells

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(8)

imagewell = imagewells.loadImageWell(resultfile="imagewell-files")
tiles = imagewell['landscape']
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

#  create, scale and place the image
x, y = 10, 10


#
# Normal Image 1
#

h = 10
x, y = 10 , h + 20

top, w, h = pb.placeImage(c, img1path, x, y, fullwidth, "Image 1", 0)

pb.label(c, "Normal Image 1", x, y)


#
# Equalize Image 1
#

x, y = 10 , h + 20 + y

top, w4, h4 = pb.placeImage(c, img1path, x, y, fullwidth, "Image 2", 1)
c.top.equalize()
pb.label(c, "Equalized Image 1", x, y)

# draw the result
c.draw(name="Layer_function_equalize")

