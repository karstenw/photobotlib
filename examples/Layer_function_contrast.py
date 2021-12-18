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
img1, w1, h1 = pb.placeImage(c, img1path, x, y, tilewidth, "Image 1")
pb.label(c, "Image 1 Contrast: 100", x, y)

#
# Image 2
#
c.layers[img1].duplicate()
c.top.name = "Image 2"
c.top.contrast(80)

x, y = w1+20, 10
c.top.translate( x, y)
pb.label(c, "Image 2 Contrast: 80", x, y)

#
# Image 3
#
c.layers[img1].duplicate()
c.top.name = "Image 3"
c.top.contrast(60)

x, y = 10, h1 + 20
c.top.translate( x, y)
pb.label(c, "Image 3 Contrast: 60", x, y)

#
# Image 4
#
c.layers[img1].duplicate()
c.top.name = "Image 4"
c.top.contrast(40)

x, y = w1+20, h1 + 20
c.top.translate( x, y)
pb.label(c, "Image 4 Contrast: 40", x, y)

#
# Image 5
#
c.layers[img1].duplicate()
c.top.name = "Image 5"
c.top.contrast(20)

x, y = 10, 2*h1 + 30
c.top.translate( x, y)
pb.label(c, "Image 3 Contrast: 20", x, y)

#
# Image 6
#
c.layers[img1].duplicate()
c.top.name = "Image 6"
c.top.contrast(10)

x, y = w1+20, 2*h1 + 30
c.top.translate( x, y)
pb.label(c, "Image 6 Contrast: 10", x, y)

#
# Image 7
#
c.layers[img1].duplicate()
c.top.name = "Image 7"
c.top.contrast(150)

x, y = 10, 3*h1 + 40
c.top.translate( x, y)
pb.label(c, "Image 7 Contrast: 150", x, y)

#
# Image 8
#
c.layers[img1].duplicate()
c.top.name = "Image 8"
c.top.contrast(200)

x, y = w1 + 20, 3*h1 + 40
c.top.translate( x, y)
pb.label(c, "Image 8 Contrast: 200", x, y)

# draw the result
c.draw(name="Layer_function_contrast")

