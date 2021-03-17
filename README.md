### PhotoBot ###

A Pillow based layered compositions library. The original version is part of the [NodeBox Library](https://github.com/karstenw/Library).


Original documentation:
[https://www.nodebox.net/code/index.php/PhotoBot](https://www.nodebox.net/code/index.php/PhotoBot)


#### Landslide ####
A Photobot demo by Tom de Smedt.
[https://www.nodebox.net/code/index.php/Landslide](https://www.nodebox.net/code/index.php/Landslide)


PhotoBot was initially a part of the NodeBox Library.

Since 2013 it has been updated to the current Python 2 and Pillow libraries.

This version works standalone with Python2.7, Python3.8 and is identical to the current NodeBox Library version.



##### Fundamental changes #####

- property `canvas.top` adresses the top layer

- property `canvas.topindex` returns the index of the top layer

- property `canvas.dup` duplicates the top layer



##### Installation #####
`python setup.py install`

##### Usage #####

T.B.D. see examples folder.

##### Hints #####

`python Kontaktabzug-1.py PATH-TO_IMAGE-FOLDER`

creates a contact print of a folder. All other Layer_* examples demonstrate a single function.

After the first usage there should be a file `imagewell.txt` which can be edited for your image folders.

