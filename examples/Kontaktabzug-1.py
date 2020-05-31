import sys, os

import pprint
pp = pprint.pprint
kwdbg = False

import pdb

# need a different name
import random as rnd

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)


import photobot as pb

# load the image library
# check for command line folders
additionals = sys.argv[1:]

# get all images from user image wells
imagewell = pb.loadImageWell(   bgsize=(1024,768),
                                minsize=(256,256),
                                pathonly=True,
                                additionals=additionals,
                                ignorelibs=True)

# tiles are images >256x256 and <=1024x768
# pp(imagewell['fractions'])
tiles = imagewell['allimages']

print "tiles:", len(tiles)


# CONFIGURATION
# A4 = 210mm x 297mm
# 150 dots/inch ~ 60 dots/cm --> 6 dots / mm

dpmm = 6

pagewidth = 210 * dpmm
pageheight = 297 * dpmm


# UNUSED
continuous = False

insettop = insetbottom = insetleft = insetright = 50

gutter = 1 * dpmm

columns = 6
rows = 9

columns = 3
rows = 5

#columns = 2
#rows = 4


# derived vars

rowwidth = pagewidth - (insetleft + insetright)
colheight = pageheight - (insettop + insetbottom)

verticalgutter = (rows-1) * gutter
horizontalgutter = (columns-1) * gutter

effectiverowheight = colheight - verticalgutter
effectivecolumnwidth = rowwidth - horizontalgutter

cellwidth = effectivecolumnwidth / float(columns)
cellheight = effectiverowheight / float(rows)


# 
pagenr = 1
pagebasename = pb.datestring()



def grid(cols, rows, colSize=1, rowSize=1, gutter=0, shuffled=False):
    """Returns an iterator that contains coordinate tuples.
    
    The grid can be used to quickly create grid-like structures.
    A common way to use them is:
        for x, y in grid(10,10,12,12):
            rect(x,y, 10,10)
    """
    # Prefer using generators.
    rowRange = xrange(int(rows))
    colRange = xrange(int(cols))
    # Shuffled needs a real list, though.
    if (shuffled):
        rowRange = list(rowRange)
        colRange = list(colRange)
        shuffle(rowRange)
        shuffle(colRange)
    for y in rowRange:
        for x in colRange:
            yield (x*colSize + x*gutter, y*rowSize + y*gutter)


def debugcanvas( c ):
    w, h = c.w, c.h
    img = pb.Image.new("RGBA", (w,h), (255,255,255,0))

    draw = pb.ImageDraw.Draw(img)
    draw.rectangle((insetleft,
                    insettop,
                    insetleft+rowwidth,
                    insettop+colheight),
                   outline=(0,0,0))
    c.layer( img, 0, 0, "DEBUG")
    del draw


# pdb.set_trace()
# 
done = False

while not done:

    pagename = "%s-%s" % (pagebasename, str(pagenr).rjust(3, "0"))
    print
    print pagename

    x0 = insettop
    y0 = insetleft

    # fill a page
    c = pb.canvas(pagewidth, pageheight)
    c.fill( (233,233,233) )
    debugcanvas( c )

    pageitems = 0

    g = grid(columns, rows, cellwidth, cellheight, gutter)
    
    for x,y in g:
        x += x0
        y += y0
        x = int( round(x) )
        y = int( round(y) )
        try:
            img = tiles.pop(0)
            print x,y,img.encode("utf-8")
        except:
            done = True
            break
        folder, filename = os.path.split( img )
        pb.placeImage(c, img, 0, 0, cellwidth, filename)
        c.top.translate(x,y)
        pageitems += 1
    # pdb.set_trace()
    if pageitems > 0:
        c.draw(name=pagename)
        pagenr +=1

