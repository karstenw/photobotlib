# heavily inspired by https://www.nodebox.net/code/index.php/Landslide
import sys, os

# need a different name
import random as rnd


import pprint
pp = pprint.pprint

import pdb
kwdbg = 0

if kwdbg:
    # make random choices repeatable for debugging
    rnd.seed(0)

W, H = 960, 1200


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


# create the canvas
c = pb.canvas( WIDTH, HEIGHT)

c.fill((210, 210, 10))


# the gradients

# SOLID
grad1idx = c.gradient(pb.SOLID, 180, 180)
c.top.translate(10, 10)
pb.label( c, "SOLID", 10, 10, 26)

# LINEAR
grad2idx = c.gradient(pb.LINEAR, 180, 180)
c.top.translate(200, 10)
pb.label( c, "LINEAR", 200, 10, 26)

# RADIAL
grad3idx = c.gradient(pb.RADIAL, 180, 180)
c.top.translate(390, 10)
pb.label( c, "RADIAL", 390, 10, 26)

# DIAMOND
grad4idx = c.gradient(pb.DIAMOND, 180, 180)
c.top.translate(580, 10)
pb.label( c, "DIAMOND", 580, 10, 26)

# SINE (from 0 to 180)
grad5idx = c.gradient(pb.SINE, 180, 180)
c.top.translate(10, 200)
pb.label( c, "SINE 0..180", 10, 200, 26)

# COSINE (from 0 to 90)
grad6idx = c.gradient(pb.COSINE, 180, 180)
c.top.translate(200, 200)
pb.label( c, "COSINE 0..90", 200, 200, 26)

# ROUNDRECT (with radius arg)
grad7idx = c.gradient(pb.ROUNDRECT, 180, 180, radius=30, radius2=30)
c.top.translate(390, 200)
pb.label( c, "ROUNDRECT", 390, 200, 26)

# RADIALCOSINE
grad8idx = c.gradient(pb.RADIALCOSINE, 180, 180)
c.top.translate(580, 200)
pb.label( c, "RADIALCOSINE", 580, 200, 26)

# QUAD
grad8idx = c.gradient(pb.QUAD, 180, 180, radius=36, radius2=36)
c.top.translate(770, 200)
pb.label( c, "QUAD", 770, 200, 26)


# the gradients masked with itself
# 
gx, xy = 180, 180
# SOLID
grad1idx = c.gradient(pb.SOLID , gx, xy)
mask = c.gradient(pb.SOLID, gx, xy)
c.top.mask()
c.top.translate(10, 390)


# LINEAR
grad2idx = c.gradient(pb.LINEAR, gx, xy)
mask = c.gradient(pb.LINEAR, gx, xy)
c.top.mask()
c.top.translate(200, 390)


# RADIAL
# you want to have the RADIAL gradient inverted
grad3idx = c.gradient(pb.RADIAL, gx, xy, radius=36)
c.top.invert()
mask = c.gradient(pb.RADIAL, gx, xy)
c.top.invert()
c.top.mask()
c.top.translate(390, 390)


# DIAMOND
grad4idx = c.gradient(pb.DIAMOND, gx, xy)
mask = c.gradient(pb.DIAMOND, gx, xy)
c.top.mask()
c.top.translate(580, 390)


# SINE 0..180
grad5idx = c.gradient(pb.SINE, gx, xy)
mask = c.gradient(pb.SINE, gx, xy)
c.top.mask()
c.top.translate(10, 580)


# COSINE 0..90
grad6idx = c.gradient(pb.COSINE, gx, xy)
mask = c.gradient(pb.COSINE, gx, xy)
c.top.mask()
c.top.translate(200, 580)


# ROUNDRECT 
grad7idx = c.gradient(pb.ROUNDRECT, gx, xy, radius=30, radius2=30)
mask = c.gradient(pb.ROUNDRECT, gx, xy, radius=30, radius2=30)
c.top.mask()
c.top.translate(390, 580)


# RADIALCOSINE
grad8idx = c.gradient(pb.RADIALCOSINE, gx, xy)
mask = c.gradient(pb.RADIALCOSINE, gx, xy)
c.top.mask()
c.top.translate(580, 580)

# QUAD
grad9idx = c.gradient(pb.QUAD, gx, xy, radius=36, radius2=9)
mask = c.gradient(pb.QUAD, gx, xy, radius=36, radius2=9)
c.top.mask()
c.top.translate(770, 580)




# COSINE 0..90
grad6idx = c.gradient(pb.COSINE, gx, xy)
mask = c.gradient(pb.COSINE, gx, xy)
c.top.mask()
c.top.translate(100, 800)
c.top.rotate(45)


# RADIALCOSINE

grad8idx = c.gradient(pb.RADIALCOSINE, gx*2, xy)
mask = c.gradient(pb.RADIALCOSINE, gx*2, xy)
c.top.mask()
c.top.translate(390, 770)


# QUAD
grad9idx = c.gradient(pb.QUAD, gx*2, xy)
mask = c.gradient(pb.QUAD, gx*2, xy)
c.top.mask()
c.top.translate(390, 960)

c.draw()
