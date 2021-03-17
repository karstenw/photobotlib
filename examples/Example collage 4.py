# heavily inspired by https://www.nodebox.net/code/index.php/Landslide
W,H = 1920, 1080
RATIO = W / H
import os
kwdbg = 0

size(W, H)

background( 0.333 )

# need a different name; random is taken
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)
    # pass

# import photobot
try:
    pb = ximport("photobot")
    pbh = ximport("pbhelpers")
except ImportError:
    pb = ximport("__init__")
    reload(pb)
from pbhelpers import *

# import extensions if nodebox version < 1.9.18
try:
    imagefiles
except NameError:
    from nodeboxExtensions import *

# create the canvas
c = pb.canvas(int(WIDTH), int(HEIGHT))

sources = [
    #u"/Volumes/Vulcan/bilder/sci-fi/2001/+screenshots",
    #u"/Volumes/Vulcan/bilder/sci-fi/2001/2017",
]

# get all images from system "Desktop Pictures" folder
filetuples = imagefiles( "/Library/Desktop Pictures", False )
# filetuples = imagefiles( "../images", False )
# filetuples = imagefiles( sources, False )

# filter out all 1 pix one color images by ignoring all files < 100k
tiles = []
for t in filetuples:
    path, filesize, lastmodified, mode, islink = t
    if filesize < 50000:
        continue
    tiles.append( path )

# shuffle the images
rnd.shuffle(tiles)
rnd.shuffle(tiles)
rnd.shuffle(tiles)


img1path = tiles.pop()
img2path = tiles.pop()


# CONFIGURATION

columns = 3
rows = 2

colwidth = int(WIDTH / columns)
rowheight = int(HEIGHT / rows)
maxsize = int(max(colwidth,rowheight)*1.2)
maxsize = int( rowheight * 1.2 )

# print "colwidth/rowheight:", colwidth, rowheight

xgutter = colwidth * 0.0667
ygutter = rowheight * 0.0667
# print "xgutter/ygutter:", xgutter, ygutter

realwidth = colwidth - 1*xgutter
realheight = rowheight - 1*ygutter 

positions = list(grid(columns, rows, colwidth, rowheight))

randomblur = not kwdbg
paintoverlay = not kwdbg


#
# Base Image
#

#  create, scale and place the image
x, y = 0, 0
top, w, h = pb.placeImage(c, img1path, x, y, W, "Image 1")


for position in positions:
    x, y = position


    # create image in canvas at 0,0
    p = tiles.pop()
    print p
    top, w, h = pb.placeImage(c, p, 0, 0, maxsize, "Image %i,%i" % (x,y)) #, width=False, height=True)

    # scale the layer to row height
    scaleLayerToHeight( c.top, rowheight )

    # uniform width
    #layer = cropImageToRatioHorizontal( layer, RATIO )

    # get the new image bounds - layer still valid
    w, h = c.top.bounds()

    # add contrast - layer still valid
    c.top.contrast(1.1)

    r = rnd.random()
    # 10%
    if 0 < r < 0.2:
        #print "20% LINEAR"
        # create gradient layer
        # top is now gradient index
        top = c.gradient(pb.LINEAR, int(w/2), h)
        c.top.flip( pb.HORIZONTAL )

        # layer + 4 flip
        # c.top.flip( pb.HORIZONTAL )

        # layer +4 translate half a pict right
        c.top.translate(w/2, 0)

        # create gradient layer
        # top is now second gradient index
        top = c.gradient(pb.LINEAR, int(w/2), h)

        # merge both gradients; destroys top layer
        c.merge([ top-1 , top ])
    elif 0.2 <= r < 0.4:
        #print "20% SINE"
        top = c.gradient(pb.SINE, w, h)
        
    elif 0.4 <= r < 0.6:
        #print "20% RADIALCOSINE"
        top = c.gradient(pb.RADIALCOSINE, w, h)
        # c.top.invert()
    elif 0.6 <= r < 0.8:
        #print "20% ROUNDRECT"
        # 25%
        top = c.gradient(pb.ROUNDRECT, w, h, "", radius=int(w/5.0), radius2=int(w/5.0))
    elif r >= 0.8:
        #print "20% QUAD"
        top = c.gradient(pb.QUAD, w, h, "", 0, 0)
            
    # print "After mask"
    c.top.brightness(1.4)
    # mask destroys top layer
    c.top.mask()

    destx = x - xgutter
    desty = y - ygutter
    # print "Image@", x, y
    # c.top.translate(destx, desty)
    c.top.translate(x, y)

    if 0: #randomblur:
        if rnd.random() > 0.75:
            #print "FLIP"
            c.top.flip()

        if rnd.random() > 0.75:
            #print "BLUR"
            c.top.blur()

if 1:
    # orange hue mask finish
    #print "Mr. Orange"
    top = c.fill((220,110,0))
    c.top.opacity(60)
    # c.top.color()
    c.top.hue()

if 0: #paintoverlay:
    # paint overlay
    #print "VINCENT"
    top = c.layer( os.path.abspath("./paint.jpg") )
    w, h = c.top.bounds()
    xs = WIDTH / float(w)
    ys = HEIGHT / float(h)
    s = max(xs,ys)
    c.top.scale(s, s)
    # c.top.opacity(50)
    c.top.overlay()



c.draw(0, 0)
