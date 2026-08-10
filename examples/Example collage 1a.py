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
nodebox = True
try:
    pb = ximport("photobot")
    size(W, H)
    background( 0.333 )
except ImportError:
    pb = ximport("__init__")
    # reload(pb)
    size(W, H)
    background( 0.333 )
except NameError:
    import photobot as pb
    pb.kwdbg = kwdbg
    pb.kwlog = kwlog
    WIDTH, HEIGHT = W, H
    nodebox = False

# identify script
fn = os.path.split( __file__ )[1]
args = str(sys.argv[1:])
if pb.py3:
    print("\n\npython3 %s  %s" %(fn, args) )
else:
    print("\n\npython2 %s  %s" %(fn, args) )


# get collage script number "collageid" for export name
collageid = "??"
# pdb.set_trace()
try:
    basename, ext = os.path.splitext( fn )
    fnwords = basename.split()
    collageid = fnwords[-1]
except Exception as err:
    print("Get collageid FAILED: '%s'" % (basename,) )
    print( err )
    
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
                             ignoreDotFolders=True,
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

columns = 5
rows = 4

enoughTiles = len(tiles) > (columns * 2 * rows)

randomblur = 0
randomflip = 0
paintoverlay = 0
gilb =0

# 
y_offset = int(round( HEIGHT / float(rows)))
x_offset = int(round( WIDTH / float(rows)))

# remove background if needed
# c.layers.pop()


tiles = []
for tile in imagewell['tiles']:
    if tile in imagewell['landscape']:
        tiles.append( tile )


tilecounter = 0
for j in range(rows):
    colw = 0 # rnd.randint( 0, 15 )
    for i in range(columns):

        if colw > WIDTH:
            break
        
        # new layer with a random image
        nextpictpath = tiles.pop()
        tilecounter += 1
        if kwlog or 1:
            pb.py23print( u"nextpictpath: %i\n%s" % (tilecounter, nextpictpath)  )
        
        if rnd.random() > 0.51:
            # square image
            if kwlog:
                print("SQUARE")
            images = pb.image2rectangles( nextpictpath, "squares" )
            img = images[0]
            top = c.layer( img )
            # print("tile:", tilecounter, w, h)
        else:
            # uniform aspect ratio 
            if kwlog:
                print("ASPECT RATIO")
            top = c.layer( nextpictpath )
            pb.cropImageToRatioHorizontal( c.top, RATIO )
                
        # get current image bounds
        w, h = c.top.bounds()
        
        # skip a tile with p < 0.2
        # rnd.random() < 0.2:
        # 0:
        # (i+j) % 2 == 0:
        if rnd.random() < 0.2:
            if kwlog:
                print("Layer POPPED", i,j)
            c.layers.pop()
            colw += w
            continue
        
        # calculate scale & apply
        s = pb.aspectRatio( (w,h), y_offset, height=True)
        c.top.scale(s, s)
        
        # add contrast
        c.top.contrast(1.1)
        
        # get the new image bounds
        w, h = c.top.bounds()
        
        if 1:
            pb.makerandomgradient( c, w, h, brighter=1.4 )
            c.top.mask()

        
        # c.top.translate(colw+i*w, j*y_offset)
        c.top.translate(colw, j*y_offset)
        c.top.opacity( 44 + rnd.random() * 29 )
        
        if randomblur:
            if rnd.random() > 0.5:
                c.top.flip()

            if rnd.random() > 0.5:
                c.top.blur()

        w, h = c.top.bounds()
        colw += w
        
        
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
    name = "photobot_" + pb.datestring() + "-" + configname + "-" + collageid
c.draw(0,0, name=name)

