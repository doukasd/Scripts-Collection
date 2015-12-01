#!/usr/bin python
# -*- coding: utf-8 -*-
""" copy_tagged_files.py

Copyright (c) 2015 Dimitris Doukas <@doukasd on github>

------------------

License:

This software is free to use in any way at your own risk.

------------------

Usage:

$copy_tagged_files.py -s <source_directory> -d <destination_directory> -t <tag>

Looks inside the <source_directory> and all subdirectories for files of accepted
extensions that have a certain <tag> and copies them to the <destination_directory>.

"""

from xattr import xattr
from sys import argv, stderr, exit
import os
import shutil
import argparse
import finder_colors

# extensions of files which we are interested in
ACCEPTED_EXTENSIONS = ['.jpg', '.jpeg', '.png']


if __name__ == '__main__':
    def process(directory):
        for root, dirs, files in os.walk(directory):
            for filename in files:
                name, ext = os.path.splitext(filename)
                if ext.lower() in ACCEPTED_EXTENSIONS:
                    check(os.path.join(root, filename))

    def check(pathname):
        if finder_colors.get(pathname) == args['tag']:
            print('Adding ' + pathname)
            try:
                shutil.copy(pathname, args['destination'])
            # eg. src and dest are the same file
            except shutil.Error as e:
                print('Error: %s' % e)
            # eg. source or destination doesn't exist
            except IOError as e:
                print('Error: %s' % e.strerror)

    # parse the args and provide feedback/help
    parser = argparse.ArgumentParser(description='Searches for files with a specific tag color in a source directory and copies them to a destination directory')
    parser.add_argument('-s','--source', help='The source directory.', required=True)
    parser.add_argument('-d','--destination', help='The destination directory.', required=True)
    parser.add_argument('-t','--tag', help='The tag to look for - i.e. green, red, etc.', required=True)
    args = vars(parser.parse_args())

    # check that the source and destination directories exist
    if not os.path.exists(args['source']):
        print('Source directory does not exist. Please provide a valid source directory.')
        exit()
    if not os.path.exists(args['destination']):
        os.makedirs(args['destination'])

    # process everything in the source directory
    process(args['source'])


