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

#print img1path.encode("utf-8")
#print img2path.encode("utf-8")

#
# Image 1
#

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


#
# Subtract Images 1 & 2
#

h = max(h1, h2)
x, y = 10 , h + 20

top, w3, h3 = pb.placeImage(c, img1path, x, y, 522, "Image 3")
top, w4, h4 = pb.placeImage(c, img2path, x, y, 522, "Image 4")
c.top.subtract_modulo()

pb.label(c, "Subtract Modulo Image 1 over Image 2", x, y)


#
# Subtract Images 2 & 1
#

h = max(h3, h4)
x, y = 10 , h + 20 + y

top, w4, h4 = pb.placeImage(c, img2path, x, y, 522, "Image 5")
top, w3, h3 = pb.placeImage(c, img1path, x, y, 522, "Image 6")
c.top.subtract_modulo()
pb.label(c, "Subtract Modulo Image 2 over Image 1", x, y)

# draw the result
c.draw()
