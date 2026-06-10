import sys, os, pdb

# need a different name
import random as rnd

import pprint
pp = pprint.pprint

import pdb
kwdbg = 1


W, H = 900, 1250
inset = 30
fullwidth = int( W - 2*inset )

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

if 0: #kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(8)

imagewell = imagewells.loadImageWell()
tiles1 = imagewell['landscape']
rnd.shuffle(tiles1)

def p(s):
    # print
    if pb.py3:
        print( s )
    else:
        print( s.encode("utf-8") )


# pick 2 images
img1path = tiles1.pop()
img1path = "/Library/Desktop Pictures/Yosemite 5.jpg"
_, filename = os.path.split( img1path )


#pdb.set_trace()
w0,h0 = imagesize( img1path, pixelsize=True )
w1,h1 = pb.aspectRatio( (w0,h0), fullwidth, height=False, width=True, assize=True)
print("\n\nsizewidth, imagewidth:", WIDTH, w1)
fullheight = 2 * h1 + 3 * inset

if NB:
    print("H - newH:", H, fullheight )
    size( W, fullheight )

# create a white canvas
c = pb.canvas( W, fullheight)
c.fill( (192, 192, 192) )

#
# Image 1
#

pb.py23print( "img1path: %s" % img1path )
#  create, scale and place the image
x, y = inset, inset
top, w1, h1 = pb.placeImage(c, img1path, x, y, fullwidth, filename)
print("x,y,w1,h1", x,y,w1,h1 )
pb.label(c, filename, x, y, 30)


# the copy layer
x = inset
y = h1 + inset + inset
_, w1, h1 = pb.placeImage(c, img1path, x, y, fullwidth, "%s inner square" % filename)

img2layer = c.top

# pdb.set_trace()
rectangles = pb.calculateRectangles(w1, h1)
rectangles = pb.explodeRectangles( rectangles )

display = []


# innersquare
if 0:
    display.append( "innersquare" )
    img2layer.duplicate()
    squarerect = rectangles.innerSquare
    #print("InnerSquare", squarerect )
    x1,y1,w,h = squarerect
    x2 = x1+w
    y2 = y1+h
    c.top.crop( ( x1, y1, x2, y2 ) )
    c.top.translate( x+x1, y+y1 )
    c.top.opacity( 65 )
    # pb.label(c, "Image 1 inner square", x, y, 30)

# quads
if 0:
    display.append( "quads" )
    quads = rectangles.quads
    
    for quad in quads:
        #print( "quad:", quad )
        img2layer.duplicate()
        c.top.scale( 0.5, 0.5 )
        c.top.translate( x+quad[0], y+quad[1] )
        c.top.opacity( 25 + rnd.random() * 30 )

# niner
if 1:
    display.append( "niner" )
    niner = rectangles.niner
    
    for nine in niner:
        #print( "niner:", nine )
        img2layer.duplicate()
        c.top.scale( 1/3.0, 1/3.0 )
        c.top.translate( x+nine[0], y+nine[1] )
        c.top.opacity( 10 + rnd.random() * 20 )
    # pb.label(c, "Image 1 niner", x, y, 30)

display = ' & '.join( display )
display = "%s - %s" % ( filename, display )

# img2layer.opacity( 10 )
img2layer.delete()

pb.label(c, display, x, y, 30)
    
# draw the result
c.draw(name="Image_innerSquare")
