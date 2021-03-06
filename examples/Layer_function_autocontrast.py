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

WIDTH, HEIGHT = 800, 1050

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
img1, w1, h1 = pb.placeImage(c, img1path, x, y, 380, "Image 1 Base")

c.layers[img1].duplicate()
c.top.autocontrast(cutoff=0)
pb.label(c, "%s autocontrast: 0" % filename, x, y)

#
# Image 2
#
c.layers[img1].duplicate()
c.top.autocontrast(cutoff=5)

x, y = w1+20, 10
c.top.translate( x, y)
pb.label(c, "%s autocontrast: 5" % filename, x, y)

#
# Image 3
#
c.layers[img1].duplicate()
c.top.autocontrast(cutoff=10)

x, y = 10, h1 + 20
c.top.translate( x, y)
pb.label(c, "%s autocontrast: 10" % filename, x, y)

#
# Image 4
#
c.layers[img1].duplicate()
c.top.autocontrast(cutoff=15)

x, y = w1+20, h1 + 20
c.top.translate( x, y)
pb.label(c, "%s autocontrast: 15" % filename, x, y)

#
# Image 5
#
c.layers[img1].duplicate()
c.top.autocontrast(cutoff=30)

x, y = 10, 2*h1 + 30
c.top.translate( x, y)
pb.label(c, "%s autocontrast: 30" % filename, x, y)

#
# Image 6
#
c.layers[img1].duplicate()
c.top.autocontrast(cutoff=35)

x, y = w1+20, 2*h1 + 30
c.top.translate( x, y)
pb.label(c, "%s autocontrast: 35" % filename, x, y)

#
# Image 7
#
c.layers[img1].duplicate()
c.top.autocontrast(42)

x, y = 10, 3*h1 + 40
c.top.translate( x, y)
pb.label(c, "%s autocontrast: 42" % filename, x, y)

#
# Image 8
#
c.layers[img1].duplicate()
c.top.autocontrast(cutoff=49)

x, y = w1 + 20, 3*h1 + 40
c.top.translate( x, y)
pb.label(c, "%s autocontrast: 49" % filename, x, y)

# draw the result
c.draw()

