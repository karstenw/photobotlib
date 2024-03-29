import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 1

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

imagewell = imagewells.loadImageWell(tabfilename=True)
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

_, fname = os.path.split( img1path )

#  create, scale and place the image
x, y = 10, 10
top, w1, h1 = pb.placeImage(c, img1path, x, y, fullwidth, fname)
pb.label(c, fname, x, y)

#
# Image 2
#
x, y = 10, 10 + h1 + 10
top, w2, h2 = pb.placeImage(c, img1path, x, y, fullwidth, fname)
c.layers[top].emboss()


pb.label(c, "%s emboss()" % fname, x, y)


# draw the result
c.draw(name="Layer_function_emboss")

