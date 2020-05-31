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

WIDTH, HEIGHT = 542, 1050


# get all images from user image wells
filetuples = pb.imagefiles( pb.imagewells(), False )
imagewell = pb.loadImageWell()
backgrounds = imagewell['backgrounds']
rnd.shuffle(backgrounds)

img1path = backgrounds.pop()
img2path = backgrounds.pop()

c = pb.canvas( WIDTH, HEIGHT)
c.fill((255, 255, 255))






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
c.draw(0, 0)
