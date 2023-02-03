from __future__ import print_function

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
kwdbg = 1
kwlog = 1
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

def uniprint( s ):
    if py3:
        print( s )
    else:
        print( s.encode("utf-8") )

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


class Pathitems:
    """A class that simply holds the most used attributes of a filepath."""

    def __init__(self, pathorname ):
        # path, folder, parent, filename, basename, ext, folderexists, fileexists
        self.setPath( pathorname )

    def setPath(self, path ):
        self.path = makeunicode( os.path.abspath( os.path.expanduser( path )))
        self.folder, filename = os.path.split( self.path )
        _, self.parent = os.path.split( self.folder )
        self.setFilename( filename, makepath=False )

    def setFilename( self, name, makepath=True ):
        self.basename, self.ext = os.path.splitext( name )
        self.filename = self.basename + self.ext 
        if makepath:
            self.setPath( os.path.join( self.folder, self.filename ) )
        self.existence()

    def setExt(self, ext):
        self.setFilename( self.basename + ext )

    def existence(self):
        self.folderexists = os.path.exists( self.folder )
        self.fileexists = os.path.exists( self.path )

    def items(self):
        return (self.path, self.folder, self.parent, self.filename,
                self.basename, self.ext, self.folderexists, self.fileexists)

    def prnt(self):
        print( "path:", self.path )
        print( "folder:", self.folder )
        print( "filename:", self.filename )
        print( "basename:", self.basename )
        print( "folderexists:", self.folderexists )
        print( "fileexists:", self.fileexists )

def filelist( folderpathorlist, ignoreDotFolders=True ):
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
                uniprint( root )
            
            # filter out parentfolders starting with '.'
            if ignoreDotFolders:
                _, foldername = os.path.split( root )
                if foldername.startswith('.'):
                    print("DOTFOLDER IGNORED:", root)
                    continue

            for thefile in files:
                thefile = makeunicode( thefile )
                basename, ext = os.path.splitext(thefile)

                doit = True
                # exclude dotfiles
                if thefile.startswith(u'.'):
                    doit = False

                # exclude the specials
                for item in (u'\r', u'\n', u'\t'):
                    if item in thefile:
                        doit = False

                # dont handle this file
                if not doit:
                    continue

                filepath = makeunicode( os.path.join( root, thefile ) )

                info = os.stat( filepath )
                lastmodf = datetime.datetime.fromtimestamp( info.st_mtime )
                islink = os.path.islink( filepath )
                record = (filepath,
                          info.st_size,
                          lastmodf,
                          oct(info.st_mode),
                          islink )
                yield record


def imagefiles( folderpathorlist, ignoreDotFolders=False ):
    """Get a list of images from a list of folders.

    folderpathorlist: is either a string with a path or a list of paths
    
    Returns a list of filetuples
    
    filetuple = (path, filesize, lastmodf, mode, islink, width, height)
    
    """

    filetuples = filelist( folderpathorlist, ignoreDotFolders=ignoreDotFolders )
    exts = ".tif .tiff .gif .jpg .jpeg .png" # + " .eps"
    extensions = tuple( exts.split() )
    for filetuple in filetuples:
        path, filesize, lastmodf, mode, islink = filetuple
        path = makeunicode( path )

        _, ext = os.path.splitext( path )
        if ext.lower() not in extensions:
            continue

        s = (-1,-1)
        try:
            img = Image.open(path)
            s = img.size
        except:
            pass #continue
        finally:
            del img

        record = (path, filesize, lastmodf, mode, islink, s[0], s[1])
        yield record


def fileisnewerthan(path1, path2):
    """Compare the file modification dates of path1 and path2.

    Return True if path1 is younger than path2.
    
    False otherwise."""
    
    try:
        info1 = os.stat( path1 )
        lastmodf1 = datetime.datetime.fromtimestamp( info1.st_mtime )

        info2 = os.stat( path2 )
        lastmodf2 = datetime.datetime.fromtimestamp( info2.st_mtime )
        
        return lastmodf1 > lastmodf2

    except:
        pass

    return False

def loadtabsfile( path ):
    """Read the iamges cache file."""
    
    if kwlog:
        print( "Reading Tabsfile..." )
    
    start = time.time()
    f = io.open(path, "r", encoding="utf-8")
    lines = f.readlines()
    f.close()
    filetuples = []
    
    for line in lines:
        path, filesize, lastmodified, mode, islink, imagewidth, imageheight = line.split( u"\t" )
        filesize = int(filesize)
        islink = bool(islink)
        imagewidth = int(imagewidth)
        imageheight = int(imageheight)
        if os.path.exists( path ):
            filetuples.append( (path, filesize, lastmodified, mode, islink, imagewidth, imageheight) )
    
    stop = time.time()
    if kwlog:
        print( "%i records loaded from Tabsfile." % len(filetuples) )
        print( "Reading Tabsfile... Done." )
        print( "READ TIME: %.3f" % (stop-start,) )        

    return filetuples


def writetabsfile( tabfilepath, filetuples ):
    """Write out the image data as tab separated text."""

    if kwlog:
        print( "Writing tabfilepath..." )
    start = time.time()
    
    tabitem = Pathitems( tabfilepath )

    # the containing folder does not exist    
    if not tabitem.folderexists:
        return False
    
    linetemplate = u"%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
    f = io.open(tabitem.path, "w", encoding="utf-8")

    for item in filetuples:
        path, filesize, lastmodified, mode, islink, width, height = item
        width = str(width)
        height = str(height)
        islink = str(int(bool(islink)))
        filesize  = str( filesize )
        item = ( path, filesize, lastmodified, mode, islink, width, height )
        f.write( linetemplate % item )
    
    f.close()
    stop = time.time()
    
    if kwlog:
        print( "Writing tabfilepath...  %s records   Done." % len(filetuples) )
        print( "WRITE TIME: %.4f" % (stop-start,) )

    return True    

#
# image well section
#

def getImageWellsFile( imagewellsfile="imagewell.txt" ):
    return os.path.abspath( imagewellsfile )


def imagewells( imagewellsfile="imagewell.txt" ):
    """Find a file named "imagewell.txt" and interpret it as image folder paths.
    If no file is found create one with the desktop image folders for
    macOS, win10 and linux.
    
    Returns: a list of folder paths
    """
    
    folders = [
        # macos system wallpapers
        "/Library/Desktop Pictures",
        
        # windows
        "C:\Windows\Web",
        
        # linux wallpapers
        "/usr/share/backgrounds",
        "/usr/share/wallpapers" ]

    fullpath = getImageWellsFile( imagewellsfile )

    # include adjacent "images" folders
    for imgfolder in ("./images", "../images"):
        images = os.path.abspath( os.path.expanduser(imgfolder) )
        if os.path.exists( images ):
            folders.append( images )

    # write new default imagewells.txt file and exit
    if not os.path.exists( fullpath ):
        try:
            f = open(fullpath, 'w')
            f.write( "\n".join( folders ) )
            f.close()
        except:
            pass
        return folders

    # read imagewells file
    try:
        with open(fullpath, 'Ur') as f:
            lines = f.readlines()
        if not lines:
            return folders
        
        # now we have read an imagewell, discard them default folders
        folders = []
        for line in lines:
            line = line.strip( "\n\r" )
            folders.append( makeunicode( line ) )
    except:
        pass

    # filter for existent folders
    folders = [x for x in folders if os.path.exists(x)]

    return folders


def loadImageWell(  bgsize=(1024,768),
                    minsize=(256,256),
                    maxfilesize=100000000,
                    maxpixellength=16000,
                    pathonly=True,
                    additionals=None,
                    ignorelibs=False,
                    imagewellfilename="imagewell.txt",
                    tabfilename="",
                    ignoreDotFolders=True,
                    ignoreFolderNames=None):

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

        imagewellfilename
            The name of the file in the scripts folder which contains the list
            of image folders.
            Defaults to "imagewell.txt"
        
        tabfilename
            The basename of the file in the scripts folder which contains the
            tab separated image records for faster image loading.
            Defaults to False
            
        ignoreFolderNames
            A list of names of folders to be ignored.


    Returns:
        A dict of dicts with several image classifications.

        list of file paths if pathonly is True
        list of filetuple records else.
    """

    # init
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
    # slope = 1.0
    
    imagecount = 0
    filetuples = []
    fileLoaded = False
    folders = []
    # <init

    imageWellsFilePath = getImageWellsFile( imagewellfilename )
    if kwlog:
        uniprint("imageWellsFilePath: %s" % imageWellsFilePath)
    
    if tabfilename == True:
        tabitem = Pathitems( imageWellsFilePath )
        tabitem.setExt(".tab")

    elif tabfilename:
        tabitem = Pathitems( tabfilename )
    else:
        tabitem = False

    imagewellitem = Pathitems( imageWellsFilePath )

    # read cached folders
    if not ignorelibs:

        # get all images from user image wells
        folders = imagewells(imagewellfilename)
        if kwlog:
            pp(folders, width=300)
        
        if tabitem:
            if tabitem.ext != ".tab":
                tabitem.setExt( ".tab" )
            if tabitem.fileexists:
                imageTabsfileIsNewer = fileisnewerthan( tabitem.path, imagewellitem.path )
                if imageTabsfileIsNewer:
                    filetuples = loadtabsfile( tabitem.path )
                    fileLoaded = True

    if additionals:
        folders.extend( additionals )

    # read the folders if filetuples are empty
    if len(filetuples) < 1:
        
        # get filetuples for all image folders
        filepathdict = dict()
        start = time.time()

        imagefilerecords = imagefiles( folders, ignoreDotFolders=ignoreDotFolders )
        for imagefilerecord in imagefilerecords:
            path, filesize, lastmodified, mode, islink, imagewidth, imageheight = imagefilerecord
            path = makeunicode(path)
            item = ( path, filesize, lastmodified, mode, islink, imagewidth, imageheight )
            if not path in filepathdict:
                filetuples.append( item )
                filepathdict[ path ] = item

        stop = time.time()
        print( "FOLDER SCAN TIME: %.3f" % (stop-start,) )

    if kwlog:
        print( "File loop..." )
    start = time.time()

    # >file loop
    for filetuple in filetuples:
        
        path, filesize, lastmodified, mode, islink, imagewidth, imageheight = filetuple

        imageitem = Pathitems( path )
        path, folder, parent, filename, basename, ext, folderexists, fileexists = imageitem.items()

        # apply all filters

        # name of parent folder starts with
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
            
        # filter minimal pixel lengths
        if ext.lower() != ".eps":
            if (imagewidth < minw) and (imageheight < minh):
                continue
            if (imagewidth > maxpixellength) or (imageheight > maxpixellength):
                continue
        
        # filter maximal pixel lengths
        if (imagewidth > maxpixellength) or (imageheight > maxpixellength):
            continue
        
        # filter max filesize
        if filesize > maxfilesize:
            continue
        
        # filter images with anormal width or height
        if imagewidth in (0, 0.0):
            print( "Anormal width: %s %i %i" % (path, imagewidth, imageheight) )
            continue
        if imageheight in (0, 0.0):
            print( "Anormal height: %s %i %i" % (path, imagewidth, imageheight) )
            continue

        # accumulate largest, smallest and median
        imagecount += 1
        # collect some stats
        if imagewidth < smallestw:
            smallestw = imagewidth
        if  imageheight < smallesth:
            smallesth = imageheight
        if imagewidth > largestw:
            largestw = imagewidth
        if  imageheight > largesth:
            largesth = imageheight
        medianw += imagewidth
        medianh += imageheight

        # now the image has survived filtering
        # sample some stats

        # categories

        # landscape or portrait
        proportion = "landscape"
        if imageheight > imagewidth:
            proportion = "portrait"
        
        # fractions
        fracs = "x:y"
        try:
            frac = Fraction(imagewidth, imageheight)
            fracs = "%i:%i" % (frac.numerator, frac.denominator )
        except TypeError as err:
            print( "FractionsError:\n", err )
            print( imagewidth )
            print( imageheight )
        
        # path or record format
        if pathonly:
            record = path
        else:
            record = (path, filesize, lastmodified, mode, islink,
                      imagewidth, imageheight, proportion, fracs)
        
        result['allimages'].append( record )
        
        # sort record into remaining categories

        # candidate has at least canvas size and can be used as background
        # otherwise it is a tile
        if (imagewidth >= bgw) and (imageheight >= bgh):
            result['backgrounds'].append( record )
        else:
            result['tiles'].append( record )
        
        if fracs not in result['fractions']:
            result['fractions'][fracs] = []
        result['fractions'][fracs].append( record )
        
        if proportion == "landscape":
            result['landscape'].append( record )
        else:
            result['portrait'].append( record )

    # <file loop


    stop = time.time()
    if kwlog:
        print( "File loop... Done." )
        print( "Fileloop: %.3f" % (stop-start,) )  

    # store largest smallest median
    result[ 'WxH largest' ] = (largestw,largesth)
    result[ 'WxH smallest' ] = (smallestw,smallesth)
    result[ 'WxH median' ] = (medianw / float(imagecount),
                              medianh / float(imagecount))

    # setup optional result file
    if tabfilename and (not fileLoaded):
        writetabsfile( tabfilename, filetuples )
    
    return result


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



