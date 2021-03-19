import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

W, H = 800, 1850
tilewidth = int((W-30) / 2.0)

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

imagewell = pb.loadImageWell(resultfile="imagewell-files")
tiles = imagewell['landscape']
rnd.shuffle(tiles)


# pick 2 images
img1path = tiles.pop()
img2path = tiles.pop()

# create a gray canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (192, 192, 192) )

#
# Image 1
#

#  create, scale and place the image
x, y = 10, 10
top, w1, h1 = pb.placeImage(c, img1path, x, y, tilewidth, "Image 1")
pb.label(c, "Image 1", x, y)

#
# Image 2
#
x, y = w1+20, 10
top, w2, h2 = pb.placeImage(c, img2path, x, y, tilewidth, "Image 2")
pb.label(c, "Image 2", x, y)



#
# Overlay Images 1 & 2
#

h = max(h1, h2)
x, y = 10 , h + 20

top, w3, h3 = pb.placeImage(c, img1path, x, y, tilewidth*2, "Image 3")
top, w4, h4 = pb.placeImage(c, img2path, x, y, tilewidth*2, "Image 4")


c.top.overlay()
pb.label(c, "Overlay Image2 over Image1", x, y)

#
# Overlay Images 2 & 1
#

h = max(h3, h4)
x, y = 10 , h + 20 + y

top, w4, h4 = pb.placeImage(c, img2path, x, y, tilewidth*2, "Image 5")
top, w3, h3 = pb.placeImage(c, img1path, x, y, tilewidth*2, "Image 6")


c.top.overlay()
pb.label(c, "Overlay Image1 over Image2", x, y)

# draw the result
c.draw()

