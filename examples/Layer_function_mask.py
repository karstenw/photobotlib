import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

W, H = 542, 1050


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
    rnd.seed(8)

imagewell = pb.loadImageWell(resultfile="imagewell-files")
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
_, w1, h1 = pb.placeImage(c, img1path, x, y, 192, "Image 1", width=True)
pb.label(c, "Image 1", x, y)

#
# Image 2
#
x, y = w1+20, 10
_, w2, h2 = pb.placeImage(c, img2path, x, y, 192, "Image 2", width=True)
pb.label(c, "Image 2", x, y)



#
# Mask Images 1 & 2
#

h = max(h1, h2)
x, y = 10 , h + 20

_, w3, h3 = pb.placeImage(c, img1path, 0, 0, 522, "Image 3", width=True)
_, w4, h4 = pb.placeImage(c, img2path, 0, 0, 522, "Image 4", width=True)
c.top.mask()
c.top.translate(x, y)

pb.label(c, "Mask Image1 over Image2", x, y)

#
# Mask Images 2 & 1
#

h = max(h3, h4)
x, y = 10 , h + 20 + y

_, w4, h4 = pb.placeImage(c, img2path, 0, 0, 522, "Image 5", width=True)
_, w3, h3 = pb.placeImage(c, img1path, 0, 0, 522, "Image 6", width=True)
c.top.mask()
c.top.translate(x, y)

pb.label(c, "Mask Image2 over Image1", x, y)

# draw the result
c.draw(name="Layer_function_mask")
