__author__ = 'doukasd'

'''
This script goes through all the images in a given directory,
crops them to a specified aspect ratio and scales them (down only)
for all the resolutions needed.

It doesn't modify GIFs as they are not supported by the Pillow library.

Purpose: Processes project images for doukasd.com
'''

import os
import re
from shutil import copy
from PIL import Image

# Settings
aspectRatio = 16.0/9.0                      # the aspect ratio to crop to, must be landscape at this point
maxScreenWidth = 720                        # the max width of the image at normal x1 DPI
maxDPIMultiplier = 2                        # typically 2
cwd = os.getcwd() + '/project-assets 2/'    # subdir to scan
targetDir = os.getcwd() + '/export/'        # subdir to export images to

# Some checks and prep
if maxDPIMultiplier < 1:
    maxDPIMultiplier = 1
if not os.path.exists(targetDir):
    os.makedirs(targetDir)
if aspectRatio < 1:
    print('WARNING: Target aspect ratio must be landscape.\n\n')


# Helper method for cropping to the landscape aspect ratio
def crop_area(image_size):
    w, h = image_size
    area = 0, 0, w, h
    if float(w)/float(h) < aspectRatio:

        # Crop to the desired aspect ratio
        target_height = int(w / aspectRatio)
        dh = int(float(h - target_height)/2.0)
        area = 0, dh, w, h - dh
        print('Crop area = ' + area.__str__())

    return area


# Get all files in the folder
fileList = os.listdir(cwd)
numImages = 0
for file in fileList:
    try:
        im = Image.open(os.path.join(cwd, file))
        print('\n')
        print(file, im.format, "%dx%d" % im.size, im.mode)
        numImages += 1

        # Create the various size versions, starting from
        # the large ones and scaling down to the smaller ones
        dpiMultiplier = maxDPIMultiplier
        while dpiMultiplier >= 1:

            # Create the filename suffix for this size
            filenameSuffix = ''
            if dpiMultiplier >= 2:
                filenameSuffix = '@' + dpiMultiplier.__str__() + 'x'

            # Create the new filename
            filename, ext = os.path.splitext(os.path.basename(os.path.join(cwd, file)))
            newFilename = filename + filenameSuffix + ext

            # Don't process GIFs via PIL as it doesn't support animation
            # just copy and rename them as needed
            if im.format == 'GIF':
                copy(os.path.join(cwd, file), os.path.join(targetDir, newFilename))
                print('Saved GIF as ' + newFilename)
            else:
                # Do any resizing needed on the rest of the images
                maxWidth = maxScreenWidth * dpiMultiplier
                w, h = im.size
                if w > maxWidth:
                    newHeight = int(h * maxWidth / w)
                    print('Resizing to ' + maxWidth.__str__() + 'x' + newHeight.__str__())
                    im = im.resize((maxWidth, newHeight), Image.ANTIALIAS)

                # Crop to the desired aspect ratio
                im = im.crop(crop_area(im.size))

                # Save
                im.save(os.path.join(targetDir, newFilename))
                print('Saved as ' + newFilename + ' at ' + im.size.__str__())

            # decrease the DPI multiplier and go again
            dpiMultiplier = dpiMultiplier - 1

    except IOError as err:
        print('Error: ' + err.strerror.__str__() + ': ' + os.path.join(cwd, file))


print('\n' + numImages.__str__() + ' images processed.\n')