import sys, os

# need a different name
import random as rnd

import photobot as pb


import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

WIDTH, HEIGHT = 542, 1050

imagewell = pb.loadImageWell()
tiles = imagewell['tiles']
rnd.shuffle(tiles)

img1path = tiles.pop()

# create the canvas
c = pb.canvas(int(WIDTH), int(HEIGHT))


#
# Image 1
#

_, fname = os.path.split( img1path )

#  create, scale and place the image
x, y = 10, 10
top, w1, h1 = pb.placeImage(c, img1path, x, y, 522, fname)
pb.label(c, fname, x, y)

#
# Image 2
#
x, y = 10, 10 + h1 + 10
top, w2, h2 = pb.placeImage(c, img1path, x, y, 522, fname)
c.layers[top].contour()


pb.label(c, "%s contour()" % fname, x, y)


# draw the result
c.draw()

