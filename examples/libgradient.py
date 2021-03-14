# -*- coding: utf-8 -*-

from __future__ import print_function
import random as rnd

# import photobot
try:
    pb = ximport("photobot")
except ImportError:
    pb = ximport("__init__")
    reload(pb)
except NameError:
    import photobot as pb


kwdbg = False

def makerandomgradient( c, w, h, y_offset ):
    r = rnd.random()
    # r = 0.01
    if kwdbg:
        print( "mask random: %.2f" % r )
    # create gradient layer
    grad = "BILINEAR"

    
    # P:0.3 - create a dual ramp gradient
    if r < 0.3:
        # c.makemask(   SOLID | LINEAR | RADIAL | DIAMOND
        #             | DUALRAMP | SINE | COSINE | RADIALCOSINE
        #             | ROUNDRECT, w, h)
        _ = c.gradient(pb.LINEAR, w/2, h)
        c.top.flip( pb.HORIZONTAL )

        # layer translate half a pict right
        c.top.translate(w/2, y_offset)

        # create another gradient layer and merge with first gradient
        topidx = c.gradient(pb.LINEAR, w/2, h)
        # merge both gradients; destroys top layer
        c.merge([ topidx-1 , topidx ])
        c.top.brightness(1.8)

    # P:0.2 - sine 0..π
    elif 0.3 <= r < 0.5:
        grad = "SINE"
        c.gradient(pb.SINE, w, h)
        
    # P:0.25 - radial cosine
    elif 0.5 <= r < 0.75:
        grad = "RADIALCOSINE"
        c.gradient(pb.RADIALCOSINE, w, h)
        # c.top.invert()

    # P:0.25 - round rect
    else:
        grad = "ROUNDRECT"
        c.gradient(pb.ROUNDRECT, w, h, radius=int(w/5.0))

    if kwdbg:
        print( "Gradient:  %s" % grad )


