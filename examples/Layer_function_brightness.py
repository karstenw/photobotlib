import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

W, H = 550, 1050


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

#  create, scale and place the image
x, y = 10, 10
img1, w1, h1 = pb.placeImage(c, img1path, x, y, 256, "Image 1")
pb.label(c, "Image 1 Brightness: 100", x, y)

#
# Image 2
#
c.layers[img1].duplicate()
c.top.name = "Image 2"
c.top.brightness(80)

x, y = w1+20, 10
c.top.translate( x, y)
pb.label(c, "Image 2 Brightness: 80", x, y)

#
# Image 3
#
c.layers[img1].duplicate()
c.top.name = "Image 3"
c.top.brightness(60)

x, y = 10, h1 + 20
c.top.translate( x, y)
pb.label(c, "Image 3 Brightness: 60", x, y)

#
# Image 4
#
c.layers[img1].duplicate()
c.top.name = "Image 4"
c.top.brightness(40)

x, y = w1+20, h1 + 20
c.top.translate( x, y)
pb.label(c, "Image 4 Brightness: 40", x, y)

#
# Image 5
#
c.layers[img1].duplicate()
c.top.name = "Image 5"
c.top.brightness(20)

x, y = 10, 2*h1 + 30
c.top.translate( x, y)
pb.label(c, "Image 3 Brightness: 20", x, y)

#
# Image 6
#
c.layers[img1].duplicate()
c.top.name = "Image 6"
c.top.brightness(10)

x, y = w1+20, 2*h1 + 30
c.top.translate( x, y)
pb.label(c, "Image 6 Brightness: 10", x, y)

#
# Image 7
#
c.layers[img1].duplicate()
c.top.name = "Image 7"
c.top.brightness(150)

x, y = 10, 3*h1 + 40
c.top.translate( x, y)
pb.label(c, "Image 7 Brightness: 150", x, y)

#
# Image 8
#
c.layers[img1].duplicate()
c.top.name = "Image 8"
c.top.brightness(200)

x, y = w1 + 20, 3*h1 + 40
c.top.translate( x, y)
pb.label(c, "Image 8 Brightness: 200", x, y)



# draw the result
c.draw(0, 0)

