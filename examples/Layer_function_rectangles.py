import sys, os

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

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


def p(s):
    # print
    if pb.py3:
        print( s )
    else:
        print( s.encode("utf-8") )


# pick 2 images
img1path = tiles.pop()
img2path = tiles.pop()

# create a white canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (192, 192, 192) )

#
# Image 1
#

p( img1path)
#  create, scale and place the image
x, y = 10, 10
top, w1, h1 = pb.placeImage(c, img1path, x, y, fullwidth, "Image 1")
pb.label(c, "Image 1", x, y, 30)

#
# image 2 - which is just image 1
#
x = 10
y = h1 + 10 + 10
_, w1, h1 = pb.placeImage(c, img1path, x, y, fullwidth, "Image 2 inner square")

img2layer = c.top

rectangles = pb.calculateRectangles(w1, h1)
rot = rnd.random() > 0.5


# innerrect
if 1:
    img2layer.duplicate()
    squarerect = rectangles.innerSquare
    x1,y1,w,h = squarerect
    x2 = x1+w
    y2 = y1+h
    c.top.crop( ( x1, y1, x2, y2 ) )
    if rot:
        c.top.rotate( -18 + rnd.random() * 36 )
    c.top.translate( x+x1, y+y1 )
    c.top.opacity( 50 )
    # pb.label(c, "Image 1 inner square", x, y, 30)

if 1:
    quads = rectangles.quads
    
    for quad in quads:
        print(quad)
        img2layer.duplicate()
        c.top.scale( 0.5, 0.5 )
        if rot:
            c.top.rotate( -18 + rnd.random() * 36 )
        c.top.translate( x+quad[0], y+quad[1] )
        c.top.opacity( 25 + rnd.random() * 30 )
    # pb.label(c, "Image 1 quads", x, y, 30)
    
if 1:
    niner = rectangles.niner
    
    for nine in niner:
        print(nine)
        img2layer.duplicate()
        c.top.scale( 1/3.0, 1/3.0 )
        if rot:
            c.top.rotate( -18 + rnd.random() * 36 )
        c.top.translate( x+nine[0], y+nine[1] )
        c.top.opacity( 10 + rnd.random() * 20 )
    # pb.label(c, "Image 1 niner", x, y, 30)

img2layer.opacity( 10 )
# img2layer.delete()
pb.label(c, "Image 1 innersquare & quads & niner", x, y, 30)

# draw the result
c.draw(name="Image_innerSquare")
