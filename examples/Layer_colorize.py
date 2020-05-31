# heavily inspired by https://www.nodebox.net/code/index.php/Landslide
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

WIDTH, HEIGHT = 532, 532

imagewell = pb.loadImageWell()
tiles = imagewell['backgrounds']
rnd.shuffle(tiles)


# pick 2 images
img1path = tiles.pop()
img2path = tiles.pop()

# create a white canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (255,255,255) )

#
# Image 1
#

#  create, scale and place the image
x, y = 10, 10
top, w1, h1 = pb.placeImage(c, img1path, x, y, 512, "Image 1")
pb.label(c, "Image 1", x, y, 30)


# apply colorize
c.top.colorize( black=(120, 120, 0),
                white=(250, 200, 96),
                  mid=(220, 190, 16))


# draw the result
c.draw(0, 0)
