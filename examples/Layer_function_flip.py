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
tiles = imagewell['landscape']
rnd.shuffle(tiles)

img1path = tiles.pop()
img2path = tiles.pop()


# create the canvas
c = pb.canvas(int(WIDTH), int(HEIGHT))
c.fill( (255,255,255) )


imsize = int((WIDTH-30)/2)
x, y = 10, 10
img1, w1, h1 = pb.placeImage(c, img1path, x, y, imsize, "image1")
pb.label(c, "Original Image", x, y)

#
# flip horizontal
#
c.layers["image1"].duplicate()
c.top.name = "flip1"

x, y = w1+20, 10
c.top.translate( x, y)
c.top.flip( pb.HORIZONTAL )
pb.label(c, "Horizontal Flip", x, y)


#
# flip vertical
#

c.layers["image1"].duplicate()
c.top.name = "flip2"
x, y = 10 , h1 + 20
c.top.flip( pb.VERTICAL )
c.top.translate( x, y )
pb.label(c, "Vertical Flip", x, y)



#
# flip horizontal & vertical
#

# duplicate does not return top
c.layers["image1"].duplicate()
c.top.name = "flip3"

x, y = w1 + 20, h1 + 20
c.top.flip( pb.HORIZONTAL | pb.VERTICAL)
c.top.translate( x, y)
pb.label(c, "Horizontal  and Vertical Flip", x, y)

# draw the result
c.draw()

