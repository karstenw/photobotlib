

"""Create all Rectangle combinations and create an image."""
import sys, random
import photobot
import imagewells
loadImageWell = imagewells.loadImageWell
imagewell = loadImageWell(   bgsize=(2048, 1440),
                             minsize=(256,256),
                             pathonly=True,
                             ignoreDotFolders=True,
                             ignoreFolderNames=('+offline', '+OFFLINE'))

# tiles are images >256x256 and <=WIDTH, HEIGHT
tiles = imagewell['tiles']

path = random.choice( tiles )
photobot.testRectangles( path, 30)

