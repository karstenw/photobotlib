# PhotoBot 0.8 beta - last updated for NodeBox 1rc4 
# Author: Tom De Smedt <tomdesmedt@trapdoor.be>
# Manual: http://nodebox.net/code/index.php/PhotoBot
# Copyright (c) 2006 by Tom De Smedt.
# Refer to the "Use" section on http://nodebox.net/code/index.php/Use

from __future__ import print_function

ALL = ['canvas', 'Layers', 'Layer', 'label', 'invertimage', 'cropimage',
    'aspectRatio', 'normalizeOrientationImage', 'insetRect',
    'cropImageToRatioHorizontal', 'scaleLayerToHeight', 'placeImage',
    'resizeImage', 'hashFromString', 'makeunicode', 'datestring', 'filelist',
    'imagefiles', 'imagewells', 'loadImageWell' ]

import sys
import os

import random
import math
sqrt = math.sqrt
pow = math.pow
sin = math.sin
cos = math.cos
degrees = math.degrees
radians = math.radians
asin = math.asin

import fractions
Fraction = fractions.Fraction

import datetime
import time
import hashlib
import unicodedata

import pickle
import json

import colorsys

import io

import PIL
import PIL.ImageFilter as ImageFilter
import PIL.Image as Image
import PIL.ImageChops as ImageChops
import PIL.ImageEnhance as ImageEnhance
import PIL.ImageOps as ImageOps
import PIL.ImageDraw as ImageDraw
import PIL.ImageStat as ImageStat
import PIL.ImageFont as ImageFont

# disable large image warning
old = Image.MAX_IMAGE_PIXELS
Image.MAX_IMAGE_PIXELS = None # 200000000
# print( "MAX_IMAGE_PIXELS: %i" % old)


import pdb
import pprint
pp = pprint.pprint
kwdbg = 0
kwlog = 0
import traceback

# py3 stuff

py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr
    long = int
    xrange = range


# PIL interpolation modes
NEAREST = Image.NEAREST
BICUBIC = Image.BICUBIC
BILINEAR = Image.BILINEAR
LANCZOS = Image.LANCZOS
INTERPOLATION = Image.BICUBIC

LAYERS = []

# blend modes
NORMAL = "normal"
MULTIPLY = "multiply"
SCREEN = "screen"
OVERLAY = "overlay"
HUE = "hue"
COLOR = "color"

ADD = "add"
SUBTRACT = "subtract"
ADD_MODULO = "add_modulo"
SUBTRACT_MODULO = "subtract_modulo"
DIFFERENCE = "difference"


HORIZONTAL = 1
VERTICAL = 2

SOLID = "solid"
LINEAR = "linear"
RADIAL = "radial"
DIAMOND = "diamond"
SCATTER = "scatter"
COSINE = "cosine"
SINE = "sine"
ROUNDRECT = "roundrect"
RADIALCOSINE = "radialcosine"
QUAD = "quad"


class Canvas:
    
    """Implements a canvas with layers.
    
    A canvas is an empty Photoshop document,
    where layers can be placed and manipulated.
    """

    def __init__(self, w, h):
        
        """Creates a new canvas.

        Creates the working area on which to blend layers.
        The canvas background is transparent,
        but a background color could be set using the fill() function.
        """
        
        self.interpolation = INTERPOLATION
        self.layers = Layers()
        self.w = w
        self.h = h
        img = Image.new("RGBA", (w,h), (255,255,255,0))
        self.layer(img, name="_bg")
        del img


    def layer(self, img, x=0, y=0, name=""):

        """Creates a new layer from file, Layer, PIL Image.

        If img is an image file or PIL Image object,
        Creates a new layer with the given image file.
        The image is positioned on the canvas at x, y.
        
        If img is a Layer,
        uses that layer's x and y position and name.
        """

        if isinstance(img, Image.Image):
            img = img.convert("RGBA")
            self.layers.append( Layer(self, img, x, y, name) )
            return len(self.layers) - 1

        if isinstance(img, Layer):
            img.canvas = self
            self.layers.append(img)
            return len(self.layers) - 1

        if type(img) in (pstr, punicode):
            try:
                img = Image.open(img)
                img = img.convert("RGBA")
                self.layers.append( Layer(self, img, x, y, name) )
                del img
                return len(self.layers) - 1
            except Exception as err:
                print( "Canvas.layer( %s ) FAILED." %repr( img ) )
                print(err)
                print()
                exc_type, exc_value, exc_tb = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_tb)
                print()
                return None


    def fill(self, rgb, x=0, y=0, w=None, h=None, name=""):

        """Creates a new fill layer.

        Creates a new layer filled with the given rgb color.
        For example, fill((255,0,0)) creates a red fill.
        The layers fills the entire canvas by default.
        """ 

        if w == None:
            w = self.w - x
        if h == None:
            h = self.h - y
        img = Image.new("RGBA", (w,h), rgb)
        result = self.layer(img, x, y, name)
        del img
        return result

    def makegradientimage(self, style, w, h):
        """Creates the actual gradient image.
        
        This has been factored out of gradient() so complex gradients like
        ROUNDRECT which consist of multiple images can be composed.
        """
        if type(w) == float:
            w *= self.w
        if type(h) == float:
            h *= self.h

        # prevent some div by 0 errors
        if w < 0:
            w = -w
        if h < 0:
            h = -h
        w = int( round( max(1,w) ))
        h = int( round( max(1,h) ))

        w2 = w // 2
        h2 = h // 2

        if kwlog:
            print( (style, self.w,self.h,w,h) )

        if style in (RADIALCOSINE, ):
            img = Image.new("L", (w, h), 0)
        elif style in (SCATTER, ):
            img = Image.new("RGBA", (w, h), (0,0,0,0))
        else:
            img = Image.new("L", (w, h), 255)

        draw = ImageDraw.Draw(img)

        if style == SOLID:
            draw.rectangle((0, 0, w, h), fill=255)

        if style == LINEAR:
            for i in xrange( w ):
                k = int( round( 255.0 * i / w ))
                draw.rectangle((i, 0, i, h), fill=k)

        if style == RADIAL:
            r = min(w,h) / 2.0
            r0 = int( round( r ))
            for i in xrange( r0 ):
                k = int( round( 255 - 255.0 * i/r ))
                draw.ellipse((w/2-r+i, h/2-r+i,
                              w/2+r-i, h/2+r-i), fill=k)
            
        if style == RADIALCOSINE:
            r = max(w,h) / 2.0
            rx = w / 2.0
            ry = h / 2.0
            r0 = int( round( r ))
            deg = 90
            base = 90 - deg
            deltaxdeg = deg / rx
            deltaydeg = deg / ry
            deltadeg = deg / r

            step = min(deltaxdeg, deltaydeg)
            for i in xrange( r0 ):
                # k = 255.0 * i/r
                k = int( round( 256 * sin( radians( base + i * deltadeg ) ) ))
                ix = i * (rx / r)
                iy = i * (ry / r)
                draw.ellipse((0 + ix, 0 + iy,
                              w - ix, h - iy), fill=k)

        if style == DIAMOND:
            maxwidthheight = int( round( max(w,h) ))
            widthradius = w * 0.5
            heightradius = h * 0.5
            for i in xrange( maxwidthheight ):
                ratio = i / float( maxwidthheight )
                x = int( round( ratio * widthradius ) )
                y = int( round( ratio * heightradius ) )
                k = int( round( 256.0 * ratio ))
                draw.rectangle((x, y, w-x, h-y), outline=k)

        if style == SCATTER:
            # scatter should be some circles randomly across WxH
            
            maxwidthheight = int( round( max(w,h) ))
            minwidthheight = int( round( min(w,h) ))
            def rnd( w, offset ):
                r = random.random()
                result = -offset + r * (w + offset + offset)
                return result

            # circles at 10%
            circleradius = int( round( minwidthheight / 10.0 ))
            c2 = 2 * circleradius
            for count in xrange( 400 ):
                x = int( round( rnd( w, circleradius ) ))
                y = int( round( rnd( h, circleradius ) ))
                k = int( round( 5 + random.random() * 127))
                draw.ellipse((x, y, x+c2, y+c2), fill=(255,255,255,k) )

        if style in (SINE, COSINE):
            # sin/cos 0...180 left to right
            action = sin
            deg = 180.0
            base = 0
            if style == COSINE:
                action = cos
                deg = 90.0
                base = 90.0 - deg
            deltadeg = deg / w
            for i in xrange( w ):
                k = int( round( 256.0 * action( radians( base + i * deltadeg ) ) ))
                draw.line( (i,0,i, h), fill=k, width=1)

        
        result = img.convert("RGBA")
        del img
        del draw
        return result


    def gradient(self, style=LINEAR, w=1.0, h=1.0, name="",
                       radius=0, radius2=0):

        """Creates a gradient layer.

        Creates a gradient layer, that is usually used together
        with the mask() function.

        All the image functions work on gradients, so they can
        easily be flipped, rotated, scaled, inverted, made brighter
        or darker, ...

        Styles for gradients are LINEAR, RADIAL, DIAMOND, SCATTER,
        SINE, COSINE and ROUNDRECT
        """

        w0 = self.w
        h0 = self.h
        if type(w) == float:
            w = int( round( w * w0 ))
        if type(h) == float:
            h = int( round( h * h0 )) 


        img = None

        if style in (SOLID, LINEAR, RADIAL, DIAMOND,
                     SCATTER, SINE, COSINE, RADIALCOSINE):
            img = self.makegradientimage(style, w, h)
            img = img.convert("RGBA")
            return self.layer(img, 0, 0, name=name)


        if style == QUAD:
            # make a rectangle with softened edges
            result = Image.new("L", ( w, h ), 255)
            
            mask = Image.new("L", ( w, h ), 255)
            draw = ImageDraw.Draw(mask)

            if radius == 0 and radius2 == 0:
                radius = w / 4.0
                radius2 = w / 10.0

            r1 = int(round( radius ))
            r2 = int(round( radius2 ))
            
            if r1 == 0:
                r1 = 1
            if r2 == 0:
                r2 = 1
            d1 = 2 * r1
            d2 = 2 * r2

            # create the base rect
            baserect = self.makegradientimage(SOLID, w-d1, h-d2)
            
            # create the vertical gradients
            verleft = self.makegradientimage(COSINE, r1, h)
            verleft = verleft.transpose(Image.FLIP_LEFT_RIGHT)
            vertright = verleft.rotate( 180 )

            # create the horizontal gradients
            # since LINEAR goes from left to right, 
            horup = self.makegradientimage(COSINE, r2, w)
            horup = horup.transpose(Image.FLIP_LEFT_RIGHT)
            hordown = horup.rotate( -90, expand=1 )
            horup = hordown.rotate( 180 )

            # assemble
            result.paste( baserect, box=( r1,   0) )
            result.paste( verleft,  box=( 0,    0) )
            result.paste( vertright,box=( w-r1, 0) )

            mask.paste( hordown,    box=( 0,    0) )
            mask.paste( horup,      box=( 0,    h-r2) )

            result = ImageChops.darker(result, mask)
            result = result.convert("RGBA")
            del mask, horup, hordown
            del baserect, verleft, vertright
            return self.layer(result, 0, 0, name=name)

        if style == ROUNDRECT:
            result = Image.new("L", ( w, h ), 255)
            r1 = int( round( radius ))
            r2 = int( round( radius2 ))
            if r1 == 0:
                r1 = 1
            if r2 == 0:
                r2 = 1
            d1 = 2 * r1
            d2 = 2 * r2

            # take 1 radial grad for the 4 corners
            corners = self.makegradientimage(RADIALCOSINE, d1, d2)

            # top left
            b = corners.copy()
            tl = b.crop( box=(0,0,r1,r2) )

            # top right
            b = corners.copy()
            tr = b.crop( box=(r1,0,d1,r2) )

            # bottom left
            b = corners.copy()
            bl = b.crop( box=(0,r2,r1,d2) )

            # bottom right
            b = corners.copy()
            br = b.crop( box=(r1,r2,d1,d2) )

            # create the base rect
            brw = w - d1
            brh = h - d2
            baserect = self.makegradientimage(SOLID, brw, brh)
            
            # create the vertical gradients
            verleft = self.makegradientimage(COSINE, r1, brh)
            verleft = verleft.transpose(Image.FLIP_LEFT_RIGHT)
            vertright = verleft.rotate( 180 )

            # create the horizontal gradients
            # since LINEAR goes from left to right, 
            horup = self.makegradientimage(COSINE, r2, brw)
            horup = horup.transpose(Image.FLIP_LEFT_RIGHT)
            hordown = horup.rotate( -90, expand=1 )
            horup = hordown.rotate( 180 )

            # assemble
            result.paste( baserect, box=( r1,     r2) )

            result.paste( hordown,  box=( r1,     0) )
            result.paste( horup,    box=( r1,     brh+r2) )

            result.paste( verleft,  box=( 0,     r2) )
            result.paste( vertright,box=( brw+r1, r2) )

            result.paste( tl,       box=( 0,     0) )
            result.paste( tr,       box=( brw+r1, 0) )
            result.paste( bl,       box=( 0,     brh+r2) )
            result.paste( br,       box=( brw+r1, brh+r2) )
            img = result.convert("RGBA")
            del corners, tl, tr, bl, br, b
            del horup, hordown
            del baserect
            del verleft, vertright
            return self.layer(img, 0, 0, name=name)


    def merge(self, layers):
        
        """Flattens the given layers on the canvas.
        
        Merges the given layers with the indices in the list
        on the bottom layer in the list.
        The other layers are discarded.
        
        """
        
        layers.sort()
        if layers[0] == 0:
            del layers[0]
        self.flatten(layers)


    def flatten(self, layers=[]):

        """Flattens all layers according to their blend modes.

        Merges all layers to the canvas, using the
        blend mode and opacity defined for each layer.
        Once flattened, the stack of layers is emptied except
        for the transparent background (bottom layer).

        """
        
        # When the layers argument is omitted,
        # flattens all the layers on the canvas.
        # When given, merges the indexed layers.
        
        # Layers that fall outside of the canvas are cropped:
        # this should be fixed by merging to a transparent background
        # large enough to hold all the given layers' data
        # (=time consuming).

        if kwlog:
            start = time.time()

        if layers == []:
            layers = xrange(1, len(self.layers))

        background = self.layers._get_bg()
        background.name = "Background"
        
        for i in layers:
            layer = self.layers[i]
        
            # Determine which portion of the canvas
            # needs to be updated with the overlaying layer.
        
            x = max(0, layer.x)
            y = max(0, layer.y)
            w = min(background.w, layer.x+layer.w)
            h = min(background.h, layer.y+layer.h)
        
            baseimage = background.img.crop( (x, y, w, h) )

            # Determine which piece of the layer
            # falls within the canvas.

            x = max(0, -layer.x)
            y = max(0, -layer.y)
            w -= layer.x
            h -= layer.y

            blendimage = layer.img.crop( (x, y, w, h) )
            lblend = blendimage.convert("L")
            bwblend = lblend.convert("1")

            # Buffer layer blend modes:
            # the base below is a flattened version
            # of all the layers below this one,
            # on which to merge this blended layer.
        
            if layer.blend == NORMAL:
                buffimage = blendimage
            elif layer.blend == MULTIPLY:
                buffimage = ImageChops.multiply(baseimage, blendimage)
            elif layer.blend == SCREEN:
                buffimage = ImageChops.screen(baseimage, blendimage)
            elif layer.blend == OVERLAY:
                buffimage = Blend().overlay(baseimage, blendimage)
            elif layer.blend == HUE:
                buffimage = Blend().hue(baseimage, blendimage)
            elif layer.blend == COLOR:
                buffimage = Blend().color(baseimage, blendimage)
            elif layer.blend == ADD:
                buffimage = ImageChops.add(baseimage, blendimage)

            elif layer.blend == SUBTRACT:
                img1 = baseimage.convert("RGB")
                img2 = blendimage.convert("RGB")
                buffimage = ImageChops.subtract(img1, img2)
                buffimage = buffimage.convert("RGBA")
                del img1, img2
                # buffimage = ImageChops.subtract(baseimage, blendimage)
                # buffimage = Blend().subtract(baseimage, blendimage)

            elif layer.blend == ADD_MODULO:
                buffimage = ImageChops.add_modulo(baseimage, blendimage)

            elif layer.blend == SUBTRACT_MODULO:
                buffimage = Blend().subtract_modulo(baseimage, blendimage)

            elif layer.blend == DIFFERENCE:
                # buffimage = ImageChops.difference(baseimage, blendimage)
                img1 = baseimage.convert("RGB")
                img2 = blendimage.convert("RGB")
                buffimage = ImageChops.difference(img1, img2)
                buffimage = buffimage.convert("RGBA")
                del img1, img2
            
            # Buffer a merge between the base and blend
            # according to the blend's alpha channel:
            # the base shines through where the blend is less opaque.
        
            # Merging the first layer to the transparent canvas
            # works slightly different than the other layers.

            # buffalpha = buffimage.split()[3]
            buffalpha = buffimage.getchannel("A")
            basealpha = baseimage.getchannel("A")
            if i == 1:
                buffimage = Image.composite(baseimage, buffimage, basealpha)
            else:
                buffimage = Image.composite(buffimage, baseimage, buffalpha)
        
            # The alpha channel becomes a composite of this layer and the base:
            # the base's (optional) tranparent background
            # is retained in arrays where the blend layer
            # is transparent as well.
        
            buffalpha = ImageChops.lighter(buffalpha, basealpha) #baseimage.split()[3])
            try:
                buffimage.putalpha(buffalpha)
            except Exception as err:
                if kwdbg:
                    pdb.set_trace()
                # TBD This needs fixing
                print("PILLOW ERROR:", err)
        
            # Apply the layer's opacity,
            # merging the buff to the base with
            # the given layer opacity.
        
            baseimage = Image.blend(baseimage, buffimage, layer.alpha)

            # Merge the base to the flattened canvas.

            x = max(0, int( round( layer.x )) )
            y = max(0, int( round( layer.y )) )
            background.img.paste(baseimage, (x,y) )
            del baseimage, buffimage, buffalpha, basealpha, blendimage

        layers = list(layers)
        layers.reverse()
        for i in layers:
            del self.layers[i].img
            del self.layers[i]

        img = Image.new("RGBA", (self.w,self.h), (255,255,255,0))
        self.layers._set_bg( Layer(self, img, 0, 0, name="_bg") )
        
        if len(self.layers) == 1:
            self.layers.append(background)
        else:
            self.layers.insert(layers[-1], background)
        del img
        
        if kwlog:
            stop = time.time()
            print("Canvas.flatten( %s ) in %.3fsec." % (repr(layers), stop-start))


    def export(self, name, ext=".png", format="PNG", unique=False):

        """Exports the flattened canvas.

        Flattens the canvas.
        PNG retains the alpha channel information.
        Other possibilities are JPEG and GIF.

        """

        start = time.time()

        if not name:
            name = "photobot_" + datestring()

        if os.sep in name:
            name = os.path.abspath( os.path.expanduser( name ))

        folder, name = os.path.split( name )

        if not folder:
            folder = os.path.abspath( os.curdir )
            folder = os.path.join( folder, "exports" )
        folder = os.path.abspath( folder )


        filename = name + ext
        if name.endswith( ext ):
            filename = name

        if not os.path.exists( folder ):
            try:
                os.makedirs( folder )
            except:
                pass
        try:
            path = os.path.join( folder, filename )
            path = os.path.abspath( path )
        except:
            pass

        if unique or os.path.exists( path ):
            path = uniquepath(folder, name, ext, nfill=2, startindex=1, sep="_", always=unique)

        if kwdbg and 0:
            # if debugging is on export each layer separately
            basename = "photobot_" + datestring() + "_layer_%i_%s" + ext

            background = self.layers._get_bg()
            background.name = "Background"
            layers = xrange(1, len(self.layers) )
            for i in layers:
                layer = self.layers[i]

                # Determine which portion of the canvas
                # needs to be updated with the overlaying layer.

                x = max(0, layer.x)
                y = max(0, layer.y)
                w = min(background.w, layer.x+layer.w)
                h = min(background.h, layer.y+layer.h)

                base = background.img.crop((0, 0, background.w, background.h))

                # Determine which piece of the layer
                # falls within the canvas.

                x = max(0, -layer.x)
                y = max(0, -layer.y)
                w -= layer.x
                h -= layer.y

                blend = layer.img.crop((x, y, w, h))

                # alpha = blend.split()[3]
                alpha = blend.getchannel("A")
                buffer = Image.composite(blend, base, alpha)

                n = basename % (i, layer.name)
                path = os.path.join( folder, n )
                buffer.save( path, format=format, optimize=False)
                print( "export() DBG: '%s'" % path.encode("utf-8") )

        self.flatten()
        self.layers[1].img.save(path, format=format, optimize=False)
        if kwlog:
            print( "export() %s" % path.encode("utf-8") )

        if kwlog:
            stop = time.time()
            print("Canvas.export(%s) in %.3f sec." % (name, stop-start))

        return path

    def draw(self, x=0, y=0, name="", ext=".png", format='PNG'):
        
        """Places the flattened canvas in NodeBox.
        
        Exports to a temporary PNG file.
        # Draws the PNG in NodeBox using the image() command.
        # Removes the temporary file.
        
        """
        #if not name:
        #    name = "photobot_" + datestring()
        #if not ext:
        #    ext = ".png"

        #folder = os.path.abspath( os.curdir )
        #folder = os.path.join( folder, "exports" )
        #if not os.path.exists( folder ):
        #    try:
        #        os.makedirs( folder )
        #    except:
        #        pass
        try:
            #filename = os.path.join( folder, name + ext )
            #filename = os.path.abspath(filename)
            # path = self.export(filename)
            path = self.export(name, ext, format)
            try:
                #if nodeboxlib:
                _ctx.image(path, x, y)
            except NameError as err:
                pass
            if 0:
                os.unlink( path )
            return path
        except Exception as err:
            print(err)
            print()
            exc_type, exc_value, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)
            print()

    def preferences(self, interpolation=INTERPOLATION):

        """Settings that influence image manipulation.

        Currently, only defines the image interpolation, which
        can be set to NEAREST, BICUBIC, BILINEAR or LANCZOS.

        """
        self.interpolation = interpolation

    #
    # Some stack operations
    # 
    # some inspiration from a forth wiki page
    # dup   ( a -- a a )
    # drop  ( a -- )
    # swap  ( a b -- b a )
    # over  ( a b -- a b a )
    # rot   ( a b c -- b c a )
    # nip   ( a b -- b ) swap drop ;
    # tuck  ( a b -- b a b ) swap over ;

    @property
    def top(self):
        """Interface to top layer.
        
        """
        return self.layers[-1]

    @property
    def topindex(self):
        """get index of top layer.
        
        """
        return len(self.layers)-1


    @property
    def dup(self):
        """Duplicate top layer/stackelement.
        
        """
        layer = self.top.copy()
        layer.canvas = self
        self.layers.append( layer )
        return self.top

    def copy(self):
        
        """Returns a copy of the canvas.
        
        """
        
        _canvas = canvas( self.w, self.h )
        _canvas.interpolation = self.interpolation
        _canvas.layers = Layers()
        _canvas.w = self.w
        _canvas.h = self.h
        for layer in self.layers:
            layercopy = layer.copy()
            layercopy.canvas = self
            _canvas.layer( layercopy )
        return _canvas


def canvas(w, h):
    return Canvas(w, h)


class Layers(list):
    
    """Extends the canvas.layers[] list so it indexes layers names.
    
    When the index is an integer, returns the layer at that  index.
    When the index is a string, returns the first layer with that name.
    
    The first element, canvas.layers[0],
    is the transparent background and must remain untouched.
    
    """
    
    def __getitem__(self, index):

        if type(index) in (int, long):
            return list.__getitem__(self, index)

        elif type(index) in (pstr, punicode):
            for layer in self:
                if layer.name == index:
                    return layer
        return None

    def _get_bg(self):
        
        return list.__getitem__(self, 0)
        
    def _set_bg(self, layer):
        
        list.__setitem__(self, 0, layer)


class Layer:
    
    """Implements a layer on the canvas.
    
    A canvas layer stores an image at a given position on the canvas,
    and all the Photoshop transformations possible for this layer:
    duplicate(), desature(), overlay(), rotate(), and so on.
    
    """
    
    def __init__(self, canvas, img, x=0, y=0, name=""):
        
        self.canvas = canvas
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.w = img.size[0]
        self.h = img.size[1]
        self.alpha = 1.0
        self.blend = NORMAL
        self.pixels = Pixels(self.img, self)
        
    def prnt(self):
        # for debugging
        print("-" * 20)
        print( "name: '%s' " % self.name.encode("utf-8") )
        print("xy: %i  %i" % (self.x, self.y) )
        print("wh: %i  %i" % (self.w, self.h) )
        print("alpha: %.2f" % self.alpha)
        print("blend: %.2f" % self.blend)
        print("-" * 20)

    def index(self):
        
        """Returns this layer's index in the canvas.layers[].
        
        Searches the position of this layer in the canvas'
        layers list, return None when not found.
        
        """
        
        for i in xrange(len(self.canvas.layers)):
            if self.canvas.layers[i] == self:
                break
        if self.canvas.layers[i] == self:
            return i
        else:
            return None

    def copy(self):
        
        """Returns a copy of the layer.
        
        This is different from the duplicate() method,
        which duplicates the layer as a new layer on the canvas.
        The copy() method returns a copy of the layer
        that can be added to a different canvas.
        
        """
        
        layer = Layer(None, self.img.copy(), self.x, self.y, self.name)
        layer.w = self.w
        layer.h = self.h
        layer.alpha = self.alpha
        layer.blend = self.blend
        
        return layer
        
    def delete(self):
        
        """Removes this layer from the canvas.
              
        """
        
        i = self.index()
        if i != None:
            del self.canvas.layers[i]
        
    def up(self):
        
        """Moves the layer up in the stacking order.
        
        """
        
        i = self.index()
        if i != None:
            del self.canvas.layers[i]
            i = min(len(self.canvas.layers), i+1)
            self.canvas.layers.insert(i, self)
            
    def down(self):
        
        """Moves the layer down in the stacking order.
        
        """
        
        i = self.index()
        if i != None:
            del self.canvas.layers[i]
            i = max(0, i-1)
            self.canvas.layers.insert(i, self)

    def bounds(self):

        """Returns the size of the layer.

        This is the width and height of the bounding box,
        the invisible rectangle around the layer.

        """

        return self.img.size

    def select(self, path, feather=True):

        """Applies the polygonal lasso tool on a layer.

        The path paramater is a list of points,
        either [x1, y1, x2, y2, x3, y3, ...]
        or [(x1,y1), (x2,y2), (x3,y3), ...]

        The parts of the layer that fall outside
        this polygonal area are cut.
        
        The selection is not anti-aliased,
        but the feather parameter creates soft edges.

        """

        w, h = self.img.size
        mask = Image.new("L", (w,h), 0)

        draw = ImageDraw.Draw(mask)
        draw.polygon(path, fill=255)

        if feather:
            mask = mask.filter(ImageFilter.SMOOTH_MORE)
            mask = mask.filter(ImageFilter.SMOOTH_MORE)
        
        
        mask = ImageChops.darker(mask, self.img.getchannel("A")) #self.img.split()[3])
        self.img.putalpha(mask)

    def mask(self):

        """Masks the layer below with this layer.

        Commits the current layer to the alpha channel of 
        the previous layer. Primarily, mask() is useful when 
        using gradient layers as masks on images below. 

        For example:
        canvas.layer("image.jpg")
        canvas.gradient()
        canvas.layer(2).flip()
        canvas.layer(2).mask()

        Adds a white-to-black linear gradient to
        the alpha channel of image.jpg, 
        making it evolve from opaque on 
        the left to transparent on the right.

        """

        if len(self.canvas.layers) < 2:
            return
        i = self.index()
        if i == 0:
            return
        
        layer = self.canvas.layers[i-1]

        alpha = Image.new("L", layer.img.size, 0)

        # Make a composite of the mask layer in grayscale
        # and its own alpha channel.

        mask = self.canvas.layers[i]        
        flat = ImageChops.darker(mask.img.convert("L"), mask.img.getchannel("A")) #mask.img.split()[3])
        alpha.paste(flat, (mask.x,mask.y))
        alpha = ImageChops.darker(alpha, layer.img.getchannel("A")) #layer.img.split()[3])
        layer.img.putalpha(alpha)

        self.delete()

    def duplicate(self):

        """Creates a copy of the current layer.

        This copy becomes the top layer on the canvas.

        """

        i = self.canvas.layer(self.img.copy(), self.x, self.y, self.name)
        clone = self.canvas.layers[i]
        clone.alpha = self.alpha
        clone.blend = self.blend
                    
    def opacity(self, a=100):
        self.alpha = a * 0.01

    def multiply(self):
        self.blend = MULTIPLY

    def add(self):
        self.blend = ADD

    def subtract(self):
        self.blend = SUBTRACT

    def add_modulo(self):
        self.blend = ADD_MODULO

    def subtract_modulo(self):
        self.blend = SUBTRACT_MODULO

    def difference(self):
        self.blend = DIFFERENCE

    def screen(self):
        self.blend = SCREEN

    def overlay(self):
        self.blend = OVERLAY
        
    def hue(self):
        self.blend = HUE
        
    def color(self):
        self.blend = COLOR
        
    def brightness(self, value=1.0):

        """Increases or decreases the brightness in the layer.

        The given value is a percentage to increase
        or decrease the image brightness,
        for example 0.8 means brightness at 80%.

        """
        if value > 5:
            value = value * 0.01
        b = ImageEnhance.Brightness(self.img) 
        self.img = b.enhance(value)

    def contrast(self, value=1.0):

        """Increases or decreases the contrast in the layer.

        The given value is a percentage to increase
        or decrease the image contrast,
        for example 1.2 means contrast at 120%.

        """
        # this crashes sometimes
        try:
            if value > 5:
                value = value * 0.01
            c = ImageEnhance.Contrast(self.img) 
            self.img = c.enhance(value)
        except:
            pass

    def desaturate(self):

        """Desaturates the layer, making it grayscale.

        Instantly removes all color information from the layer,
        while maintaing its alpha channel.

        """

        # alpha = self.img.split()[3]
        alpha = self.img.getchannel("A")
        self.img = self.img.convert("L")
        self.img = self.img.convert("RGBA")
        self.img.putalpha(alpha)

    def colorize(self, black, white, mid=None,
                       blackpoint=0, whitepoint=255, midpoint=127):

        """Use the ImageOps.colorize() on desaturated layer.
        
        """
        # 
        # alpha = self.img.split()[3]
        alpha = self.img.getchannel("A")
        img = self.img.convert("L")
        img = ImageOps.colorize(img, black, white, mid,
                                     blackpoint=0, whitepoint=255, midpoint=127)
        img = img.convert("RGBA")
        img.putalpha(alpha)
        self.img = img

    def posterize(self, bits=8):
        alpha = self.img.getchannel("A")
        img = self.img.convert("RGB")
        img = ImageOps.posterize(img, bits)
        img = img.convert("RGBA")
        img.putalpha(alpha)
        self.img = img

    def solarize(self, threshhold):
        # alpha = self.img.split()[3]
        alpha = self.img.getchannel("A")
        img = self.img.convert("RGB")
        img = ImageOps.solarize(img, threshhold)
        img = img.convert("RGBA")
        img.putalpha(alpha)
        self.img = img

    def autocontrast(self, cutoff=0, ignore=None):
        if 0: #not (1 <= bits <= 8):
            return
        # alpha = self.img.split()[3]
        alpha = self.img.getchannel("A")
        img = self.img.convert("RGB")
        img = ImageOps.autocontrast(img, cutoff, ignore)
        img = img.convert("RGBA")
        img.putalpha(alpha)
        self.img = img

    def deform( self, deformer, resample=LANCZOS ):
        self.img = ImageOps.deform(self.img, deformer, resample)

    def equalize(self, mask=None):
        alpha = self.img.getchannel("A")
        img = self.img.convert("RGB")
        img = ImageOps.equalize(img, mask)
        img = img.convert("RGBA")
        img.putalpha(alpha)
        self.img = img

    def invert(self):

        """Inverts the layer.

        """
        self.img = invertimage( self.img )

    def translate(self, x, y):

        """Positions the layer at the given coordinates.

        The x and y parameters define where to position 
        the top left corner of the layer,
        measured from the top left of the canvas.

        """

        self.x = int( round( x ))
        self.y = int( round( y ))

    def scale(self, w=1.0, h=1.0):

        """Resizes the layer to the given width and height.

        When width w or height h is a floating-point number,
        scales percentual, 
        otherwise scales to the given size in pixels.

        """
        w0, h0 = self.img.size
        if type(w) == float:
            w = int( round( w*w0 ) )
        if type(h) == float:
            h = int( round( h*h0 ) )
        self.img = self.img.resize((w,h), resample=LANCZOS)
        self.w = w
        self.h = h

    def rotate(self, angle):

        """Rotates the layer.

        Rotates the layer by given angle.
        Positive numbers rotate counter-clockwise,
        negative numbers rotate clockwise.

        Rotate commands are executed instantly,
        so many subsequent rotates will distort the image.

        """

        # When a layer rotates, its corners will fall
        # outside of its defined width and height.
        # Thus, its bounding box needs to be expanded.

        # Calculate the diagonal width, and angle from
        # the layer center.  This way we can use the
        # layers's corners to calculate the bounding box.
        
        
        def mid( t1, t2, makeint=True ):
            # calculate the middle between t1 and t2
            return int( round( (t2-t1) / 2.0 ))

        w0, h0 = self.img.size
        diag0 = sqrt(pow(w0,2) + pow(h0,2))
        d_angle = degrees(asin((w0*0.5) / (diag0*0.5)))

        angle = angle % 360
        if (    angle >   90
            and angle <= 270):
            d_angle += 180

        w = sin(radians(d_angle + angle)) * diag0
        w = max(w, sin(radians(d_angle - angle)) * diag0)
        w = int( round( abs(w) )) 

        h = cos(radians(d_angle + angle)) * diag0
        h = max(h, cos(radians(d_angle - angle)) * diag0)
        h = int( round( abs(h) ))

        diag1 = int( round( diag0 ))

        # The rotation box's background color
        # is the mean pixel value of the rotating image.
        # This is the best option to avoid borders around
        # the rotated image.

        bg = ImageStat.Stat(self.img).mean
        bg = (int(bg[0]), int(bg[1]), int(bg[2]), 0)

        box = Image.new("RGBA", (diag1,diag1), bg)
        
        dw02 = mid( w0, diag0 ) # (diag0-w0)/2
        dh02 = mid( h0, diag0 ) # (diag0-h0)/2
        box.paste(self.img, (dw02, dh02))
        box = box.rotate(angle, Image.BICUBIC)
        
        dw2 = mid(w, diag0) # int( (diag0-w) / 2.0 )
        dh2 = mid(h, diag0) #int( (diag0-h) / 2.0 )
        box = box.crop(( dw2+2, dh2, diag1-dw2, diag1-dh2))
        self.img = box

        # Since rotate changes the bounding box size,
        # update the layers' width, height, and position,
        # so it rotates from the center.
        
        self.x += mid( w, self.w ) # int( (self.w-w)/2.0 )
        self.y += mid( h, self.h ) # int( (self.h-h)/2.0 )
        self.w = w
        self.h = h   

    def distort(self, x1=0,y1=0, x2=0,y2=0, x3=0,y3=0, x4=0,y4=0):

        """Distorts the layer.
        
        Distorts the layer by translating 
        the four corners of its bounding box to the given coordinates:
        upper left (x1,y1), upper right(x2,y2),
        lower right (x3,y3) and lower left (x4,y4).
        
        """

        w, h = self.img.size
        quad = (-x1,-y1, -x4,h-y4, w-x3,w-y3, w-x2,-y2)
        # quad = (x1,y1, x2,y2, x3,y3, x4,y4) #, LANCZOS)
        self.img = self.img.transform(self.img.size, Image.QUAD, quad)

    def flip(self, axis=HORIZONTAL):

        """Flips the layer, either HORIZONTAL or VERTICAL.

        """

        if axis & HORIZONTAL:
            self.img = self.img.transpose(Image.FLIP_LEFT_RIGHT)
        if axis & VERTICAL:
            self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)

    def crop( self, bounds):

        """Crop a pillow image at bounds(left, top, right, bottom)

        """
        w0, h0 = self.img.size
        x, y = self.x, self.y
        left, top, right, bottom = bounds
        left = max(x, left)
        top = max(y, top)
        right = min(right, w0)
        bottom = min(bottom, h0)
        self.img = self.img.crop( (left, top, right, bottom) )
        self.w, self.h = self.img.size

    def blur(self):
        
        """Blurs the layer.
        
        """

        self.img = self.img.filter(ImageFilter.BLUR)

    def boxblur(self, radius=2):
        
        """Blurs the layer.
        
        """

        self.img = self.img.filter( ImageFilter.BoxBlur( radius ) )

    # new
    def contour(self):
        
        """Contours the layer.
        
        """

        self.img = self.img.filter(ImageFilter.CONTOUR)

    # new
    def detail(self):
        
        """Details the layer.
        
        """

        self.img = self.img.filter(ImageFilter.DETAIL)

    # new
    def edge_enhance(self):
        
        """Edge enhances the layer.
        
        """

        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE)

    # new
    def edge_enhance_more(self):
        
        """Edge enhances more the layer.
        
        """

        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # new
    def emboss(self):
        
        """Embosses the layer.
        
        """

        self.img = self.img.filter(ImageFilter.EMBOSS)

    # new
    def find_edges(self):
        
        """Find edges in the layer.
        
        """

        alpha = self.img.getchannel("A")
        self.img = self.img.filter(ImageFilter.FIND_EDGES)
        self.img = self.img.convert("RGBA")
        self.img.putalpha(alpha)

    # new
    def smooth(self):
        
        """Smoothes the layer.
        
        """

        self.img = self.img.filter(ImageFilter.SMOOTH)

    # new
    def smooth_more(self):
        
        """Smoothes the layer more.
        
        """

        self.img = self.img.filter(ImageFilter.SMOOTH_MORE)

    def sharpen(self, value=1.0):

        """Increases or decreases the sharpness in the layer.

        The given value is a percentage to increase
        or decrease the image sharpness,
        for example 0.8 means sharpness at 80%.

        """
     
        s = ImageEnhance.Sharpness(self.img) 
        self.img = s.enhance(value)
        
    def convolute(self, kernel, scale=None, offset=0):
        
        """A (3,3) or (5,5) convolution kernel.
        
        The kernel argument is a list with either 9 or 25 elements,
        the weight for each surrounding pixels to convolute.
        
        """
        
        if len(kernel)   ==  9: size = (3,3)
        elif len(kernel) == 25: size = (5,5)
        else:                   return
        
        if scale == None:
            scale = 0
            for x in kernel:
                scale += x
            if scale == 0:
                scale = 1
        
        f = ImageFilter.Kernel(size, kernel, scale=scale, offset=offset)
        
        # alpha = self.img.split()[3]
        alpha = self.img.getchannel("A")
        img = self.img.convert("RGB")
        # f = ImageFilter.BuiltinFilter()
        # f.filterargs = size, scale, offset, kernel
        
        img = img.filter(f)
        img = img.convert("RGBA")
        img.putalpha( alpha )
        self.img = img

    def statistics(self):
        
        alpha = self.img.getchannel("A")
        return ImageStat.Stat(self.img, alpha) #self.img.split()[3])
        
    def levels(self):
        
        """Returns a histogram for each RGBA channel.
        
        Returns a 4-tuple of lists, r, g, b, and a.
        Each list has 255 items, a count for each pixel value.
                
        """
        
        h = self.img.histogram()
        r = h[0:255]
        g = h[256:511]
        b = h[512:767]
        a = h[768:1024]
        
        return r, g, b, a

class Blend:
    
    """Layer blending modes.
    
    Implements additional blending modes to those present in PIL.
    These blending functions can not be used separately from
    the canvas.flatten() method, where the alpha compositing
    of two layers is handled.
    
    Since these blending are not part of a C library,
    but pure Python, they take forever to process.
    
    """
    
    def subtract(self, img1, img2, scale=1.0, offset=0):
        base = img1.convert("RGB")
        blend = img2.convert("RGB")
        result = ImageChops.subtract(base, blend, scale=scale, offset=offset)
        result = result.convert("RGBA")
        return result

    def subtract_modulo(self, img1, img2):
        base = img1.convert("RGB")
        blend = img2.convert("RGB")
        result = ImageChops.subtract_modulo(base, blend)
        result = result.convert("RGBA")
        return result

    def overlay(self, img1, img2):

        """Applies the overlay blend mode.

        Overlays image img2 on image img1.
        The overlay pixel combines multiply and screen:
        it multiplies dark pixels values and screen light values.
        Returns a composite image with the alpha channel retained.

        """

        p1 = list( img1.getdata() )
        p2 = list( img2.getdata() )

        for i in xrange(len(p1)):
        
            p3 = ()
            for j in xrange(len(p1[i])):

                a = p1[i][j] / 255.0
                b = p2[i][j] / 255.0
            
                # When overlaying the alpha channels,
                # take the alpha of the most transparent layer.
            
                if j == 3:
                    # d = (a+b) * 0.5
                    # d = a
                    d = min(a,b)
                elif a > 0.5:
                    d = 2 * (a+b - a*b)-1
                else:
                    d = 2*a*b            
                p3 += ( int( round(d * 255.0)), )
        
            p1[i] = p3
        
        img = Image.new("RGBA", img1.size, 255)
        img.putdata(p1)
        return img

    def hue(self, img1, img2):

        """Applies the hue blend mode.

        Hues image img1 with image img2.
        The hue filter replaces the hues of pixels in img1
        with the hues of pixels in img2.
        Returns a composite image with the alpha channel retained.

        """

        p1 = list(img1.getdata())
        p2 = list(img2.getdata())

        for i in xrange(len(p1)):
        
            r1, g1, b1, a1 = p1[i]
            r1 = r1 / 255.0
            g1 = g1 / 255.0
            b1 = b1 / 255.0
        
            h1, s1, v1 = colorsys.rgb_to_hsv(r1, g1, b1)
        
            r2, g2, b2, a2 = p2[i]
            r2 = r2 / 255.0
            g2 = g2 / 255.0
            b2 = b2 / 255.0
            h2, s2, v2 = colorsys.rgb_to_hsv(r2, g2, b2)
        
            r3, g3, b3 = colorsys.hsv_to_rgb(h2, s1, v1)
        
            r3 = int( round( r3*255.0 ))
            g3 = int( round( g3*255.0 ))
            b3 = int( round( b3*255.0 ))
            p1[i] = (r3, g3, b3, a1)

        img = Image.new("RGBA", img1.size, 255)
        img.putdata(p1)
        return img

    def color(self, img1, img2):

        """Applies the color blend mode.

        Colorize image img1 with image img2.
        The color filter replaces the hue and saturation of pixels in img1
        with the hue and saturation of pixels in img2.
        Returns a composite image with the alpha channel retained.

        """
        p1 = list(img1.getdata())
        p2 = list(img2.getdata())
        for i in xrange(len(p1)):
        
            r1, g1, b1, a1 = p1[i]
            r1 = r1 / 255.0
            g1 = g1 / 255.0
            b1 = b1 / 255.0
        
            h1, s1, v1 = colorsys.rgb_to_hsv(r1, g1, b1)
        
            r2, g2, b2, a2 = p2[i]
            r2 = r2 / 255.0
            g2 = g2 / 255.0
            b2 = b2 / 255.0
            h2, s2, v2 = colorsys.rgb_to_hsv(r2, g2, b2)
        
            r3, g3, b3 = colorsys.hsv_to_rgb(h2, s2, v1)
        
            r3 = int( round( r3*255.0 ))
            g3 = int( round( g3*255.0 ))
            b3 = int( round( b3*255.0 ))

            p1[i] = (r3, g3, b3, a1)

        img = Image.new("RGBA", img1.size, 255)
        img.putdata(p1)
        return img

class Pixels:
    
    """Provides direct access to a layer's pixels.
    
    The layer.pixels[] contains all pixel values
    in a 1-dimensional array.
    Each pixel is a tuple containing (r,g,b,a) values.
    
    After the array has been updated, layer.pixels.update()
    must be called for the changes to commit.
    
    """
    
    def __init__(self, img, layer):
        
        self.layer = layer
        self.img = img
        self.data = None
        
    def __getitem__(self, i):

        w, h = self.img.size
        noofpixels = w * h
        if i >= noofpixels:
            i -= noofpixels
        if i < 0:
            i += noofpixels
        
        if self.data == None:
            self.data = list(self.img.getdata())
        return self.data[i]
        
    def __setitem__(self, i, rgba):
        
        w, h = self.img.size
        noofpixels = w * h
        if i >= noofpixels:
            i -= noofpixels
        if i < 0:
            i += noofpixels
        
        if self.data == None:
            self.data = list(self.img.getdata())
        self.data[i] = rgba

    def __iter__(self):
        
        for i in xrange(len(self)):
            yield self[i]

    def __len__(self):
        
        w, h = self.img.size
        return w * h
                    
    def update(self):
        
        if self.data != None:
            self.img.putdata(self.data)
            self.data = None
        
    def convolute(self, kernel, scale=None, offset=0):
        
        """A (3,3) or (5,5) convolution kernel.
        
        The kernel argument is a list with either 9 or 25 elements,
        the weight for each surrounding pixels to convolute.
        
        """
        
        if len(kernel)   ==  9: size = (3,3)
        elif len(kernel) == 25: size = (5,5)
        else:                   return
        
        if scale == None:
            scale = 0
            for x in kernel:
                scale += x
            if scale == 0:
                scale = 1
     
        # f = ImageFilter.BuiltinFilter()
        # f.filterargs = size, scale, offset, kernel
        f = ImageFilter.Kernel(size, kernel, scale=scale, offset=offset)
        self.layer.img = self.layer.img.filter(f)

#
# nodebox & standalone pillow tools
#

def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    typ = type(s)
    
    # convert to str first; for number types etc.
    if typ not in (punicode,):
        if typ not in (pstr,):
            s = str(s)
        try:
            s = punicode( s, srcencoding )
        except TypeError as err:
            # pdb.set_trace()
            print( "makeunicode(): %s" % repr(err) )
            print( "%s - %s" % (type(s), repr(s)) )
            return s
    if typ in (punicode,):
        s = unicodedata.normalize(normalizer, s)
    return s


def uniquepath(folder, filenamebase, ext, nfill=1, startindex=1, sep="_", always=False):
    folder = os.path.abspath( folder )
    if not always:
        path = os.path.join(folder, filenamebase + ext )
        if not os.path.exists( path ):
            return path
    n = startindex
    while True:
        serialstring = str(n).rjust(nfill, "0")
        filename = filenamebase + sep + serialstring + ext
        fullpath = os.path.join(folder, filename)
        if n >= 10**nfill:
            nfill = nfill + 1
        if not os.path.exists(fullpath):
            return fullpath
        n += 1


def hashFromString( s ):
    h = hashlib.sha1()
    h.update( s )
    return h.hexdigest()


def datestring(dt = None, dateonly=False, nospaces=True, nocolons=True):
    """Make an ISO datestring. The defaults are good for using the result of
    'datestring()' in a filename.
    """
    if not dt:
        now = str(datetime.datetime.now())
    else:
        now = str(dt)
    if not dateonly:
        now = now[:19]
    else:
        now = now[:10]
    if nospaces:
        now = now.replace(" ", "_")
    if nocolons:
        now = now.replace(":", "")
    return now


#
# image tools section
#

def invertimage( img ):
    # alpha = img.split()[3]
    alpha = img.getchannel("A")
    img = img.convert("RGB")
    img = ImageOps.invert(img)
    img = img.convert("RGBA")
    img.putalpha(alpha)
    return img


def cropimage( img, bounds):

    """Crop a pillow image at bounds(left, top, right, bottom)
    
    """
    return img.crop( bounds )


def splitimage( img, hor=1, vert=1):
    """Split a PIL image hor times horizontally and vert times vertically.
    
    Return a (hor+1) * (vert+1) list with images.
    """
    pass


def aspectRatio(size, maxsize, height=False, width=False, assize=False):
    """Resize size=(w,h) to maxsize.
    use height == maxsize if height==True
    use width == maxsize if width==True
    use max(width,height) == maxsize if width==height==False
    
    """
    w, h = size
    scale = 1.0
    
    if width !=False:
        currmax = w
    elif height !=False:
        currmax = h
    else:
        currmax = max( (w,h) )
    if width and height:
        currmax = min( (w,h) )
    if currmax == maxsize:
        # return 1.0
        pass
    elif maxsize == 0:
        #return 1.0
        pass
    else:
        scale = float(maxsize) / currmax
        w = int( round( w*scale ) )
        h = int( round( h*scale ) )
        size = (w,h)
    if assize:
        return size
    return scale


def innerRect( w0, h0, w1, h1):
    """Create an inner size crop rect (0,0,w1,h1) + translation
    """
    pass


def insetRect( rectangle, horInset, vertInset):

    """
    """
    x, y, w, h = rectangle
    dh = horInset / 2.0
    dv = vertInset / 2.0
    return x+dh, y+dv, w-horInset, h-vertInset


def cropImageToRatioHorizontal( layer, ratio ):
    
    """
    """
    w, h = layer.bounds()
    newwidth = int( round( h*ratio ))
    d = int( newwidth / 2.0 )
    x,y,w,h = insetRect( (0,0,w,h), d, 0 )
    layer.img = layer.img.crop(box=(x,y,x+w,y+h))
    return layer


def scaleLayerToHeight( layer, newheight ):
    # get current image bounds
    w, h = layer.bounds()
    # calculate scale & apply
    s = aspectRatio( (w,h), newheight, height=True)
    layer.scale(s, s)
    return layer


def placeImage(canv, path, x, y, maxsize=None, name="", width=True, height=False):
    """Create an image layer.
    
    """
    if maxsize:
        img1 = resizeImage(path, maxsize, width=width, height=height)
        top = canv.layer(img1, name=name)
    else:
        top = canv.layer(path, name=name)
    canv.top.translate(x, y)
    w, h, = canv.top.bounds()
    return top, w, h


def resizeImage( filepath, maxsize, orientation=True, width=True, height=True):

    """Get a downsampled image for use in layers.
    """
    f = False
    try:
        img = Image.open(filepath)
    except Exception as err:
        print("\nresizeImage() Image.open() FAILED '%s'" % filepath.encode("utf-8"))
        print(err)
        return ""

    # downsample the image
    if maxsize:
        w,h = aspectRatio( (img.size), maxsize,
                            height=height, width=height, assize=True)
        img = img.resize( (w,h), resample=Image.LANCZOS)
    # respect exif orientation
    if orientation:
        img = normalizeOrientationImage( img )
    if f:
        f.close()
    return img.convert("RGBA")


def normalizeOrientationImage( img ):
    """Rotate an image according to exif info.
    
    """
    rotation = 0
    try:
        info = img._getexif()
        if 274 in info:
            r = info[274]
            if r == 3:
                rotation = 180
            elif r == 6:
                rotation = -90
            elif r == 8:    
                rotation = 90
    except (Exception, IndexError) as err:
        pass
    if rotation != 0:
        return img.rotate( rotation )
    return img


#
# text section
#

def label( canvas, string, x, y, fontsize=18, fontpath="" ):
    """Needs to be written...

    """
    
    # search for a usable font
    systemarials = [
        "C:\Windows\Fonts\arial.ttf",
        "/Library/Fonts/Arial.ttf"]
    
    systemarials.insert(0, fontpath)
    font = False
    for f in systemarials:
        if os.path.exists( f ):
            font = f
            break
    
    if not font:
        return False

    w,h = canvas.w, canvas.h
    mask = Image.new("L", (w, h), 0)
    blatt = Image.new("RGBA", (w, h), (0,0,0,0))

    drawtext = ImageDraw.Draw( blatt )
    drawmask = ImageDraw.Draw( mask )

    # use a bitmap font
    font =  PIL.ImageFont.truetype(font=font, size=fontsize, index=0, encoding='')
    drawtext.text((x, y), string, font=font, fill=(192,192,192,255))
    drawmask.text((x, y), string, font=font, fill=192)
    drawtext.text((x-1, y-1), string, font=font, fill=(0,0,0,255))
    drawmask.text((x-1, y-1), string, font=font, fill=255)
    
    canvas.layer( blatt )
    canvas.layer( mask )
    canvas.top.mask()


#
# folderscanner section
#

def filelist( folderpathorlist, pathonly=True ):
    """Walk a folder or a list of folders and return
    paths or ((filepath, size, lastmodified, mode) tuples..
    """

    folders = folderpathorlist
    if type(folderpathorlist) in (pstr, punicode):
        folders = [folderpathorlist]
    result = []
    for folder in folders:
        for root, dirs, files in os.walk( folder ):
            root = makeunicode( root )
            if kwlog:
                print (root.encode("utf-8"))
            for thefile in files:
                thefile = makeunicode( thefile )
                basename, ext = os.path.splitext(thefile)

                # exclude dotfiles
                if thefile.startswith(u'.'):
                    continue

                # exclude the specials
                for item in (u'\r', u'\n', u'\t'):
                    if item in thefile:
                        continue

                filepath = os.path.join( root, thefile )
                filepath = filepath.encode("utf-8")

                record = filepath
                if not pathonly:
                    info = os.stat( filepath )
                    lastmodf = datetime.datetime.fromtimestamp( info.st_mtime )
                    islink = os.path.islink( filepath )
                    record = (filepath,
                              info.st_size,
                              lastmodf,
                              oct(info.st_mode),
                              islink )
                yield record


def imagefiles( folderpathorlist, pathonly=True ):
    """Get a list of images from a list of folders.

    folderpathorlist: is either a string with a path or a list of paths
    
    pathonly: if True return list of fullpath
              else: return a list of filetuples
    filetuple = 
        (path, filesize, lastmodf, mode, islink, width, height)
    
    """
    filetuples = filelist( folderpathorlist, pathonly=pathonly )
    exts = ".tif .tiff .gif .jpg .jpeg .png" # + " .eps"
    extensions = tuple( exts.split() )
    for filetuple in filetuples:
        path = filetuple
        if not pathonly:
            path = filetuple[0]
        path = makeunicode( path )

        _, ext = os.path.splitext( path )
        if ext.lower() not in extensions:
            continue
        if pathonly:
            # print (path.encode("utf-8"))
            yield path
        else:
            path, filesize, lastmodf, mode, islink = filetuple
            s = (-1,-1)
            try:
                img = Image.open(path)
                s = img.size
                del img
            except:
                pass #continue
            filetuple = (path, filesize, lastmodf, mode, islink, s[0], s[1])
            # print (path.encode("utf-8"))
            yield filetuple


#
# image well section
#

def getImageWellsFile( imagewellsfile="imagewell.txt" ):
    return os.path.abspath( imagewellsfile )


def imagewells( imagewellsfile="imagewell.txt" ):
    """Find a file named "imagewell.txt" and interpret it as image folder paths.
    If no file is found create one with the desktop image folders for
    mac & win10.
    
    """
    folders = [
        # macos system wallpapers
        "/Library/Desktop Pictures",
        
        # windows
        "C:\Windows\Web",
        
        # linux wallpapers
        "/usr/share/backgrounds",
        "/usr/share/wallpapers" ]

    images = os.path.abspath( "images" )
    if os.path.exists( images ):
        folders.append( images )
    fullpath = getImageWellsFile( imagewellsfile )
    
    if not os.path.exists( fullpath ):
        try:
            f = open(fullpath, 'w')
            f.write( "\n".join( folders ) )
            f.close()
        except:
            pass
        return folders
    try:
        with open(fullpath, 'Ur') as f:
            lines = f.readlines()
        if not lines:
            return folders
        folders = []
        for line in lines:
            line = line.strip("\n\r")
            folders.append( makeunicode( line ) )
    except:
        pass
    folders = [x for x in folders if os.path.exists(x)]
    return folders

class Imagecollection(object):
    """
    ImageCollection should be the return value of loadImageWell() and
    transparently handle the imagewell.txt pickling.

    The folders in imagewell.txt should be parsed, if one of the folders
    is newer or imagewell.txt is newer than imagewell-files.pick.

    """

    def __init__(self):
        self.data = {}
    
    

def loadImageWell( bgsize=(1024,768), minsize=(256,256),
                   maxfilesize=100000000, maxpixellength=16000,
                   pathonly=True, additionals=None, ignorelibs=False,
                   imagewellsfile="imagewell.txt",
                   resultfile=False, ignoreFolderNames=None):

    """
    Find images imagewells or additional folders. 
       
    Params:
        bgsize
            tuple with width and height for images to be classified background

        minsize
            tuple with minimal width and height for images not to be ignored

        maxfilesize
            in bytes. Images above this file size will be ignored

        maxpixellength
            in pixels. Images above in either dimension will be ignored

        pathonly
            return path or record
        additionals
            list of folders to me considered for this run

        ignorelibs
            if imagewells file should be ignored

    Returns:
        A dict of dicts with several image classifications.

        list of file paths if pathonly is True
        list of file records else.
    """

    tiles = []
    backgrounds = []
    proportions = {}
    fractions = {}

    result = {
        'allimages': [],
        'tiles': [],
        'backgrounds': [],
        'landscape': [],
        'portrait': [],
        'fractions': {},
        'WxH largest': "",
        'WxH smallest': "",
        'WxH median': "",
    }

    minw, minh = minsize
    bgw, bgh = bgsize
    smallestw, smallesth = 99999,99999
    largestw, largesth = 0,0
    medianw, medianh = 0,0
    slope = 1.0
    imagecount = 0
    filetuples = []

    fileLoaded = False

    imageWellsFile = getImageWellsFile( imagewellsfile )
    imageTabsfileIsNewer = False


    # pdb.set_trace()
    if ignorelibs == False:
        if not additionals:
            if resultfile != False:
                path = os.path.abspath( resultfile )
                folder, filename = os.path.split( path )
                tabfile = os.path.join( folder, filename + ".tab" )
                if os.path.exists( tabfile ):
                    try:
                        info1 = os.stat( imageWellsFile )
                        lastmodf1 = datetime.datetime.fromtimestamp( info1.st_mtime )

                        info2 = os.stat( tabfile )
                        lastmodf2 = datetime.datetime.fromtimestamp( info2.st_mtime )
                        
                        imageTabsfileIsNewer = lastmodf2 > lastmodf1
                    except:
                        pass

                    if imageTabsfileIsNewer:
                        print("Reading tabfile...")
                        start = time.time()
                        f = io.open(tabfile, "r", encoding="utf-8")
                        lines = f.readlines()
                        f.close()
                        filetuples = []

                        for line in lines:
                            path, filesize, lastmodified, mode, islink, w0, h0 = line.split( u"\t" )
                            filesize = int(filesize)
                            islink = bool(islink)
                            w0 = int(w0)
                            h0 = int(h0)
                            if os.path.exists( path ):
                                filetuples.append( (path, filesize, lastmodified, mode, islink, w0, h0) )

                        fileLoaded = True
                        stop = time.time()
                        if kwlog:
                            print("%i records loaded from tabfile." % len(filetuples))
                            print("Reading tabfile... Done.")
                            print( "READ TIME: %.3f" % (stop-start,) )        


    # get all images from user image wells
    folders = []
    if not ignorelibs:
        folders = imagewells()

    if additionals:
        folders.extend( additionals )

    # check if it has read the cache
    if not filetuples:
        start = time.time()
        filetuples = []
        items = list( imagefiles( folders, pathonly=False ) )
        for filetuple in items:
            path, filesize, lastmodified, mode, islink, w0, h0 = filetuple
            path = makeunicode(path)
            item = ( path, filesize, lastmodified, mode, islink, w0, h0 )
            filetuples.append( item )
        stop = time.time()
        print("FOLDER SCAN TIME: %.3f" % (stop-start,))

    if kwlog:
        print("File loop...")

    # pdb.set_trace()
    for t in filetuples:
        path, filesize, lastmodified, mode, islink, w0, h0 = t
        path = makeunicode( path )
        folder, filename = os.path.split( path )
        root, parent =  os.path.split( folder )
        basename, ext = os.path.splitext( filename )

        # parent names
        cancel = False
        if ignoreFolderNames:
            for name in ignoreFolderNames:
                if parent.startswith( name ):
                    cancel = True
                    # print("IGNORE PARENT: %s  %s" % (name,path))
                    break
        if cancel:
            continue
            
        # filter minimal pixel lengths
        if ext.lower() != ".eps":
            if (w0 < minw) and (h0 < minh):
                continue
            if (w0 > maxpixellength) or (h0 > maxpixellength):
                continue

        # filter maximal pixel lengths
        if (w0 > maxpixellength) or (h0 > maxpixellength):
            continue

        # filter max filesize
        if filesize > maxfilesize:
            continue

        # filter images with anormal width or height
        if w0 in (0, 0.0):
            print( "Anormal width: %s %s %s" % (repr(path),
                                                repr(w0), repr(h0)))
            continue
        if h0 in (0, 0.0):
            print( "Anormal height: %s %s %s" % (repr(path),
                                                 repr(w0), repr(h0)))
            continue

        imagecount += 1

        # collect some stats
        if w0 < smallestw:
            smallestw = w0
        if  h0 < smallesth:
            smallesth = h0
        if w0 > largestw:
            largestw = w0
        if  h0 > largesth:
            largesth = h0

        medianw += w0
        medianh += h0

        proportion = "landscape"
        if h0 > w0:
            proportion = "portrait"

        fracs = "x:y"
        try:
            frac = Fraction(w0, h0)
            fracs = "%i:%i" % (frac.numerator, frac.denominator )
        except TypeError as err:
            print(err)
            print(w0)
            print(h0)

        if pathonly:
            record = path
        else:
            record = (path, filesize, lastmodified, mode, islink,
                      w0, h0, proportion, frac)

        result['allimages'].append( record )

        # candidate has at least canvas size and can be used as background
        # otherwise it is a tile
        if (w0 >= bgw) and (h0 >= bgh):
            result['backgrounds'].append( record )
        else:
            # print( "TILE: %i < %i  and  %i < %i" % (w0,bgw,h0,bgh) )
            result['tiles'].append( record )

        if fracs not in result['fractions']:
            result['fractions'][fracs] = []
        result['fractions'][fracs].append( record )

        if proportion == "landscape":
            result['landscape'].append( record )
        else:
            result['portrait'].append( record )

    if kwlog:
        print("File loop... Done.")

    result[ 'WxH largest' ] = (largestw,largesth)
    result[ 'WxH smallest' ] = (smallestw,smallesth)
    result[ 'WxH median' ] = (medianw / float(imagecount),
                              medianh / float(imagecount))

    if resultfile and not fileLoaded:
        print("Writing tabfile...")

        path = os.path.abspath( resultfile )
        folder, filename = os.path.split( path )
        
        if os.path.exists( folder ):
            start = time.time()
            tabfile = os.path.join( folder, filename + ".tab" )
            items = []
            template = u"%s\t%s\t%s\t%s\t%i\t%i\t%i\n"
            f = io.open(tabfile, "w", encoding="utf-8")
            for item in filetuples:
                path, filesize, lastmodified, mode, islink, w0, h0 = item
                w0 = int(w0)
                h0 = int(h0)
                islink = int(bool(islink))
                filesize  = str( filesize )
                item = ( path, filesize, lastmodified, mode, islink, w0, h0 )
                f.write( template % item )
            f.close()
            stop = time.time()
            if kwlog:
                print("Writing tabfile... Done.")
                print("WRITE TIME: %.3f" % (stop-start,) )        


    return result


