import sys
import os
import io
import time
import datetime
import unicodedata

import fractions
Fraction = fractions.Fraction

import pdb
import pprint
pp = pprint.pprint
kwdbg = 0
kwlog = 0
import traceback

import PIL
import PIL.Image as Image

__all__ = ['imagewells', 'loadImageWell']


# py3 stuff

py3 = False
try:
    unicode
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


def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    typ = type(s)
    
    # convert to str first; for number types etc.
    if typ not in ( pstr, punicode ):
        s = str(s)
    if typ not in ( punicode, ):
        try:
            s = punicode(s, srcencoding)
        except TypeError as err:
            print( "makeunicode():", err )
            print( type(s), repr(s) )
    if typ in (punicode,):
        s = unicodedata.normalize(normalizer, s)
    return s


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
                print( root.encode("utf-8") )
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
            # print( path.encode("utf-8") )
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
            # print( path.encode("utf-8") )
            yield filetuple


#
# image well section
#

def getImageWellsFile( imagewellsfile="imagewell.txt" ):
    return os.path.abspath( imagewellsfile )


def imagewells( imagewellsfile="imagewell.txt" ):
    """Find a file named "imagewell.txt" and interpret it as image folder paths.
    If no file is found create one with the desktop image folders for
    macOS, win10 and linux.
    
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
            line = line.strip( "\n\r" )
            folders.append( makeunicode( line ) )
    except:
        pass
    folders = [x for x in folders if os.path.exists(x)]
    return folders


# TBD
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
            tuple with width and height for images to be classified
            as background.

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

    # >init
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
    # <init

    if ignorelibs == False:
        if not additionals:
            if resultfile != False:
                path = os.path.abspath( resultfile )
                folder, filename = os.path.split( path )
                tabfile = os.path.join( folder, filename + ".tab" )
                if os.path.exists( tabfile ):
                    # >check file dates
                    try:
                        info1 = os.stat( imageWellsFile )
                        lastmodf1 = datetime.datetime.fromtimestamp( info1.st_mtime )

                        info2 = os.stat( tabfile )
                        lastmodf2 = datetime.datetime.fromtimestamp( info2.st_mtime )
                        
                        imageTabsfileIsNewer = lastmodf2 > lastmodf1
                    except:
                        pass
                    # <check file dates

                    if imageTabsfileIsNewer:
                        # >load tabs file
                        if kwlog:
                            print( "Reading tabfile..." )

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
                            print( "%i records loaded from tabfile." % len(filetuples) )
                            print( "Reading tabfile... Done." )
                            print( "READ TIME: %.3f" % (stop-start,) )        
                        # <load tabs file


    # >read image folders
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
        print( "FOLDER SCAN TIME: %.3f" % (stop-start,) )
    # <read image folders


    if kwlog:
        print( "File loop..." )

    # >file loop
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
                    # print( "IGNORE PARENT: %s  %s" % (name,path) )
                    break
        if cancel:
            continue
            

        if ext.lower() != ".eps":
            if (w0 < minw) and (h0 < minh):
                continue
            if (w0 > maxpixellength) or (h0 > maxpixellength):
                continue



        if (w0 > maxpixellength) or (h0 > maxpixellength):
            continue


        if filesize > maxfilesize:
            continue


        if w0 in (0, 0.0):
            print( "Anormal width: %s %s %s" % (repr(path),
                                                repr(w0), repr(h0)) )
            continue

        if h0 in (0, 0.0):
            print( "Anormal height: %s %s %s" % (repr(path),
                                                 repr(w0), repr(h0)) )
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
            print( err )
            print( w0 )
            print( h0 )


        if pathonly:
            record = path
        else:
            record = (path, filesize, lastmodified, mode, islink,
                      w0, h0, proportion, fracs)


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
    # <file loop


    if kwlog:
        print( "File loop... Done." )

    result[ 'WxH largest' ] = (largestw,largesth)
    result[ 'WxH smallest' ] = (smallestw,smallesth)
    result[ 'WxH median' ] = (medianw / float(imagecount),
                              medianh / float(imagecount))

    if resultfile and not fileLoaded:
        print( "Writing tabfile..." )

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
                print( "Writing tabfile... Done." )
                print( "WRITE TIME: %.3f" % (stop-start,) )


    return result


