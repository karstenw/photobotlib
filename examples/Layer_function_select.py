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

WIDTH, HEIGHT = 600, 1050

imagewell = pb.loadImageWell()
tiles = imagewell['backgrounds']
rnd.shuffle(tiles)

img1path = tiles.pop()
img2path = tiles.pop()


# create the canvas
c = pb.canvas(int(WIDTH), int(HEIGHT))
c.fill( (255, 255, 255) )

#
# Image 1
#

_, filename = os.path.split( img1path )

#  create, scale and place the image
x, y = 10, 10
img1, w1, h1 = pb.placeImage(c, img1path, x, y, WIDTH-20, "Image 1 Base")

c.top.autocontrast(cutoff=0)
pb.label(c, filename, x, y)

#
# Image 2
#
c.layers[img1].duplicate()

path=( (w1/2,0), (w1,int(h1*0.667)), (0,h1),(0,h1/2) )
c.top.select( path )

x, y = 10, h1+20+10
c.top.translate( x, y)


# draw the result
c.draw()

