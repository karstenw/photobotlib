import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

W, H = 800, 1050


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

_, filename = os.path.split( img1path )

#  create, scale and place the image
x, y = 10, 10
img1, w1, h1 = pb.placeImage(c, img1path, x, y, 256, "Image 1 Base")

c.layers[img1].duplicate()
c.top.posterize(8)
pb.label(c, "%s posterize: None" % filename, x, y)

#
# Image 2
#
c.layers[img1].duplicate()
c.top.posterize(7)

x, y = w1+20, 10
c.top.translate( x, y)
pb.label(c, "%s posterize: 7" % filename, x, y)

#
# Image 3
#
c.layers[img1].duplicate()
c.top.posterize(6)

x, y = 10, h1 + 20
c.top.translate( x, y)
pb.label(c, "%s posterize: 6" % filename, x, y)

#
# Image 4
#
c.layers[img1].duplicate()
c.top.posterize(5)

x, y = w1+20, h1 + 20
c.top.translate( x, y)
pb.label(c, "%s posterize: 5" % filename, x, y)

#
# Image 5
#
c.layers[img1].duplicate()
c.top.posterize(4)

x, y = 10, 2*h1 + 30
c.top.translate( x, y)
pb.label(c, "%s posterize: 4" % filename, x, y)

#
# Image 6
#
c.layers[img1].duplicate()
c.top.posterize(3)

x, y = w1+20, 2*h1 + 30
c.top.translate( x, y)
pb.label(c, "%s posterize: 3" % filename, x, y)

#
# Image 7
#
c.layers[img1].duplicate()
c.top.posterize(2)

x, y = 10, 3*h1 + 40
c.top.translate( x, y)
pb.label(c, "%s posterize: 2" % filename, x, y)

#
# Image 8
#
c.layers[img1].duplicate()
c.top.posterize(1)

x, y = w1 + 20, 3*h1 + 40
c.top.translate( x, y)
pb.label(c, "%s posterize: 1" % filename, x, y)

# draw the result
c.draw()

