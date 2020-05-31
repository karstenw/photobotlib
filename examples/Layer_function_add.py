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


WIDTH, HEIGHT = 550, 1050


# get all images from user image wells
filetuples = pb.imagefiles( pb.imagewells(), False )
imagewell = pb.loadImageWell()
tiles = imagewell['landscape']
rnd.shuffle(tiles)


# CONFIGURATION

# create the canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (255, 255, 255) )

img1path = tiles.pop()
img2path = tiles.pop()


#
#
# Image 1

#  create, scale and place the image
x, y = 10, 10
top, w1, h1 = pb.placeImage(c, img1path, x, y, 256, "Image 1")
pb.label(c, "Image 1", x, y)

#
# Image 2
#
x, y = w1+20, 10
top, w2, h2 = pb.placeImage(c, img2path, x, y, 256, "Image 2")
pb.label(c, "Image 2", x, y)

yskip = max( h1, h2 )

#
# Add Images 1 & 2
#

x, y = 10 , 1 * (yskip + 20)
top, w1, h1 = pb.placeImage(c, img1path, x, y, 522, "Image 3")
top, w2, h2 = pb.placeImage(c, img2path, x, y, 522, "Image 4")
c.top.add()

yskip = h1 # max( h1, h2 )

pb.label(c, "Add Image 2 over Image 1", x, y)


#
# Screen Images 2 & 1
#

x, y = 10 , y + yskip + 20
top, w2, h2 = pb.placeImage(c, img2path, x, y, 522, "Image 5")
top, w3, h3 = pb.placeImage(c, img1path, x, y, 522, "Image 6")
c.top.add()

pb.label(c, "Add Image 1 over Image 2", x, y)

# draw the result
c.draw(0, 0)

