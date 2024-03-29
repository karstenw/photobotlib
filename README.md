## PhotoBot ##

A Pillow based layered compositions library. The original version is part of the [NodeBox Library](https://github.com/karstenw/Library).


Original documentation:
[https://www.nodebox.net/code/index.php/PhotoBot](https://www.nodebox.net/code/index.php/PhotoBot)


### Landslide ###
A Photobot demo by Tom de Smedt.
[https://www.nodebox.net/code/index.php/Landslide](https://www.nodebox.net/code/index.php/Landslide)


PhotoBot was initially a part of the NodeBox Library.

Since 2013 it has been updated to the current Python 2/3 and Pillow libraries.

This version works standalone with Python2.7, Python3.11 and is identical to the current [NodeBox Library](https://github.com/karstenw/Library) version.


#### Fundamental changes ####

`canvas.draw()` has a double functionality. In Nodebox1 it places the result in the content section of the document window.

The image is also written out to a folder "exports" with a name like "photobot_YYYY-MM-DD_HHMMSS.png" using the current datetimestamp.

If run from the Terminal, only the exports part is done.

If the exports folder does not fit your needs use canvas.export() as follows:

`cv.export( name="/Full/Path/to/image.png", ext=".png", format="PNG" )`

Extension and format follow [Pillow Image.save](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save) rules



#### New functions & properties ####

- property `canvas.top` adresses the top layer

- property `canvas.topindex` returns the index of the top layer

- property `canvas.dup` duplicates the top layer



#### Installation ####
`python setup.py install`


#### Usage ####

T.B.D. see examples folder.

#### Hints ####

`python Kontaktabzug-1.py PATH-TO_IMAGE-FOLDER`

creates a contact print of a folder. All other Layer_* examples demonstrate a single function.



#### Scanning your images with ImageWells ####

The collage examples make use of the yet unreleased "ImageWells" library of which a preliminary version is included in the examples folder.

Abbreviated example from "Example collage 1.py"

```Python

import imagewells
loadImageWell = imagewells.loadImageWell


imagewell = loadImageWell(
				bgsize=(1280, 1024),
				minsize=(256,256),
				pathonly=True,
				maxfilesize=100000000,
				maxpixellength=16000,
				additionals=additionals,
				imagewellfilename="imagewell.txt",
				tabfilename="imagewell.tab",
				ignoreDotFolders=False,
				ignoreFolderNames=('+offline',))

```


After a script uses `loadImageWell()` for the first time there should be a file `imagewell.txt` in the same folder as the script excuting.


#### The file `imagewell.txt` looks like this: ####

```
/Library/Desktop Pictures
C:\Windows\Web
/usr/share/backgrounds
/usr/share/wallpapers
```
Each line represents a path for a platform. The file is NL terminated and UTF-8 encoded.

The first line is the "Desktop Pictures" folder on macos.

Line 2 is for windows.

Lines 3+4 are for linux.

If a folder does not exist, it will be ignored. The idea is to put your own image folders into that file.



#### The parameters for loadImageWell are as follows: ####

- bgsize=(w,h) - a tuple marking the size at which a image is designated 'background'. Usually the canvas size.

- minsize=(w,h) - at least width>=w or height>=h for a image to be considered. If both are smaller, the image is ignored.

- pathonly=True|False - if False, a tuple with: (path, filesize, lastmodified, mode, islink, w0, h0, proportion, frac) is returned.

- addtionals=('folder',) - a list of folders to be added. If this is active, no caching is used.

- imagewellfilename="imagewell.txt" - the name of the folderlist file to be read.

- tabfilename="imagewell.tab" - the name of the resulting cache file.

- ignoreDotFolders=False - ignore folders starting with a '.'.  This is for MacOS '.thumbnails' folders which you usually want to ignore

- ignoreFolderNames=('folder',) - a list of folder names. If a scanned folder STARTS with a name from that list, it will be ignored.


#### The resulting dictionary contains the following keys: ####


- allimages - a list of all images

- tiles - a list of images with: minsize <= image <= bgsize

- backgrounds - a list of images considered backgrounds

- landscape - a list of images where WIDTH >= HEIGHT

- portrait - a list of images where WIDTH < HEIGHT

- fractions - dictionary with all the fractions as keys. A fraction key looks like: '1024:575', '4:3' or '16:9'. 

- 'WxH largest', 'WxH smallest' and 'WxH median': accumulated sizes

	- 'WxH largest': (8003, 5622),
	- 'WxH median': (1074.9886462882096, 754.4748180494905),
	- 'WxH smallest': (566, 167),

The items of each image list key will depend on the `pathonly` parameter.


### Examples ###

See "examples/Example collage *.py"

![](./demo-images/photobot_2021-06-10_144446.png?raw=True)

![](./demo-images/photobot_2021-06-10_144727.png?raw=True)

![](./demo-images/photobot_2021-06-10_144808.png?raw=True)


See "examples/Layer\_function\_*.py"

![](./demo-images/Layer_function_add_modulo.png?raw=True)

![](./demo-images/Layer_function_add.png?raw=True)

![](./demo-images/Layer_function_autocontrast.png?raw=True)

![](./demo-images/Layer_function_boxblur.png?raw=True)

![](./demo-images/Layer_function_brightness.png?raw=True)

![](./demo-images/Layer_function_color.png?raw=True)

![](./demo-images/Layer_function_contour.png?raw=True)

![](./demo-images/Layer_function_contrast.png?raw=True)

![](./demo-images/Layer_function_difference.png?raw=True)

![](./demo-images/Layer_function_emboss.png?raw=True)

![](./demo-images/Layer_function_enhance_more.png?raw=True)

![](./demo-images/Layer_function_enhance.png?raw=True)

![](./demo-images/Layer_function_find_edges.png?raw=True)

![](./demo-images/Layer_function_flip.png?raw=True)

![](./demo-images/Layer_function_hue.png?raw=True)

![](./demo-images/Layer_function_mask.png?raw=True)

![](./demo-images/Layer_function_multiply.png?raw=True)

![](./demo-images/Layer_function_opacity.png?raw=True)

![](./demo-images/Layer_function_overlay.png?raw=True)

![](./demo-images/Layer_function_posterize.png?raw=True)

![](./demo-images/Layer_function_screen.png?raw=True)

![](./demo-images/Layer_function_select.png?raw=True)

![](./demo-images/Layer_function_solarize.png?raw=True)

![](./demo-images/Layer_function_subtract_modulo.png?raw=True)

![](./demo-images/Layer_function_subtract.png?raw=True)


