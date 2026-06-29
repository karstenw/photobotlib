# heavily inspired by https://www.nodebox.net/code/index.php/Landslide

from __future__ import print_function

import sys, os

import pprint
pp = pprint.pprint
kwdbg = 0
kwlog = 0
if kwdbg:
    import pdb

# need a different name for nodebox
import random as rnd

import libgradient
import imagewells
loadImageWell = imagewells.loadImageWell
imagewells.kwdbg = kwdbg
imagewells.kwlog = kwlog

if kwdbg and 1:
    # make random choices repeatable for debugging
    rnd.seed( 123456 )
    

# width and height of destination image
# W, H =  800,  600
# W, H = 1024,  768
# W, H = 1280,  800
# W, H = 1440,  900
W, H = 1920, 1080
# W, H = 2560, 1440

# import photobot lib
nodebox=True
try:
    pb = ximport("photobot")
    size(W, H)
    background( 0.333 )
except ImportError:
    pb = ximport("__init__")
    reload(pb)
    size(W, H)
    background( 0.333 )
except NameError:
    import photobot as pb
    pb.kwdbg = kwdbg
    pb.kwlog = kwlog
    WIDTH, HEIGHT = W, H
    nodebox=False

if not nodebox:
    if pb.py3:
        print("\n\npython3 %s  %s" %(__file__, sys.argv[1:]) )
    else:
        print("\n\npython2 %s  %s" %(__file__, sys.argv[1:]) )



###
### This section should move into imagewells
###

# I use several distinct image collections

# the defaults
configname = ""
pathsfilename = "imagewell.txt"
storagefilename = "imagewell.tab"
additionals = []

# add configs or folders
for item in sys.argv[1:]:
    # try path
    path = os.path.abspath( os.path.expanduser( item ) )
    
    if os.path.exists( path ):
        additionals.append( path )
        continue
    
    if item not in ('',):
        # if given multiple config names only the last survives
        pathsfilename = "imagewell-" + item + '.txt'
        storagefilename = "imagewell-" + item + '.tab'
        configname = item

if kwlog or 1:
    print("configname:", configname)
    print("pathsfilename:", pathsfilename)
    print("storagefilename:", storagefilename)


# used in some examples
RATIO = WIDTH / HEIGHT


# get all images from user image wells
imagewell = loadImageWell(   bgsize=(WIDTH, HEIGHT),
                             minsize=(256,256),
                             pathonly=True,
                             additionals=additionals,
                             imagewellfilename=pathsfilename,
                             tabfilename=storagefilename,
                             ignoreDotFolders=False,
                             ignoreFolderNames=('+offline', '+OFFLINE'))

# tiles are images >256x256 and <=WIDTH, HEIGHT
tiles = imagewell['tiles']

# backgrounds are images >W,H
backgrounds = imagewell['backgrounds']


print( "tiles: %i" % len(tiles) )
print( "backgrounds: %i" % len(backgrounds) )


# create the canvas
c = pb.canvas( WIDTH, HEIGHT)
c.fill( (127,127,127) )


if not kwdbg:
    turns = int( round(20 + (rnd.random() * 10)) )
    if kwlog:
        print( "shuffle turns: %i" % turns )
    for turn in range( turns ):
        rnd.shuffle(tiles)
        rnd.shuffle(backgrounds)


# background image
if len(backgrounds) > 0:
    bgimage = backgrounds.pop()
    pb.placeImage(c, bgimage, 0, 0, WIDTH, "Image 1", width=True, height=True)
    print( "Background:")
    pb.py23print(bgimage)



# CONFIGURATION

columns = 9
rows = 4

colwidth = int(WIDTH / columns)
rowheight = int(HEIGHT / rows)
maxsize = int(max(colwidth,rowheight)*1.2)
maxsize = int( rowheight * 1.2 )

xgutter = colwidth * 0.0667
ygutter = rowheight * 0.0667

realwidth = colwidth - 1*xgutter
realheight = rowheight - 1*ygutter 

positions = list(pb.grid(columns, rows, colwidth, rowheight, shuffled=True))
# positions.extend( list(pb.grid(columns, rows, colwidth, rowheight, shuffled=True)) )
# positions.extend( list(pb.grid(columns, rows, colwidth, rowheight, shuffled=True)) )

randomblur = 0 # not kwdbg
paintoverlay = 0 # not kwdbg
gilb = 0

#
# Base Image
#

#  create, scale and place the image
x, y = 0, 0

tilecounter = 0
for position in positions:
    x, y = position

    # create image in canvas at 0,0
    nextpictpath = tiles.pop()
    tilecounter += 1
    if kwlog or 1:
        pb.py23print( u"%i - %s" % (tilecounter, nextpictpath)  )

    top, w, h = pb.placeImage(c, nextpictpath, 0, 0, maxsize=None, name="Image %i,%i" % (x,y))


    # scale the layer to row height
    if rnd.random() > 0.5:
        # random row height 0.5 <= x <= 4.5
        tileheight = rowheight * (0.5 + rnd.random() * (rows-1))
    else:
        # random row height is integer multiple
        choices = range( 1, rows+1 ) # (1,2,3,4,5)
        tileheight = rowheight * rnd.choice( choices )
    pb.scaleLayerToHeight( c.top, tileheight )

    # get the new image bounds
    w, h = c.top.bounds()
    halfwidth = int(round(w/2.0))

    
    # add contrast
    c.top.contrast(1.1)


    if kwdbg:
        print("LINEAR")

    # create up and downramp mask
    top = c.gradient(pb.LINEAR, halfwidth, h)
    c.top.flip( pb.HORIZONTAL )
    c.top.translate(halfwidth, 0)
    top = c.gradient(pb.LINEAR, halfwidth, h)
    c.merge([ top-1 , top ])

    # print "After mask"
    c.top.brightness(1.4)

    # mask destroys top layer
    c.top.mask()


    destx = x - xgutter
    desty = y - ygutter
    c.top.translate(x, y)

    
    c.top.opacity( 50 + rnd.random() * 50 )


    doflip = randomblur
    if doflip:
        # do not flip if using comic tiles
        if "/comic/" not in nextpictpath:
            if rnd.random() > 0.75:
                c.top.flip()

    if randomblur:
        if rnd.random() > 0.75:
            c.top.blur()

    if rnd.random() > 0.9:
        if kwdbg:
            print("BLEND SCREEN")
        c.top.screen()

    if rnd.random() > 0.9:
        if kwdbg:
            print("BLEND COLOR")
        c.top.color()

if gilb:
    # orange hue overlay finish
    # create new color layer
    if kwlog and 1:
        print("Orange gilb start")
    c.flatten()
    c.fill((200,100,0))
    c.top.opacity(30)
    c.top.hue()
    if kwlog and 1:
        print("Orange gilb end")


paintfile = os.path.abspath("./paint.jpg")
if paintoverlay:
    # paint overlay
    if os.path.exists( paintfile ):
        if kwdbg or 1:
            print( "paint overlay start")
        c.flatten()
        topidx = c.layer( paintfile )
        w, h = c.top.bounds()
        xs = WIDTH / float(w)
        ys = HEIGHT / float(h)
        s = max(xs,ys)
        c.top.scale(s, s)
        c.top.opacity( 90 )
        c.top.overlay()
        if kwdbg or 1:
            print( "paint overlay end")

name = ""
if configname:
    name = "photobot_" + pb.datestring() + "-" + configname
c.draw(0,0, name=name)

