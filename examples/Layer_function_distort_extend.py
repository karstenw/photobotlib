import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 1

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

imagewell = imagewells.loadImageWell(tabfilename=True)
tiles = imagewell['landscape']
rnd.shuffle(tiles)


import PIL

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

#
# Normal Image 1
#

h = 10
x, y = 10 , h + 20

top, w, h = pb.placeImage(c, img2path, x, y, fullwidth, "Image 1", 0)

pb.label(c, "Normal Image 1", x, y)


#
# distort Image 1
#

x, y = 10 , h + 20 + y

top, w4, h4 = pb.placeImage(c, img2path, x, y, fullwidth, "Image 2", 1)

class Example:
    def getdata(self):
        method = PIL.Image.Transform.EXTENT
        data = (-50, -50, 550, 550)
        return method, data

# x1=0,y1=0, x2=w,y2=0, x3=w,y3=h, x4=0,y4=h
c.top.distort( method=Example() )
pb.label(c, "Distorted Image 1", x, y)

# draw the result
c.draw(name="Layer_function_distort")

