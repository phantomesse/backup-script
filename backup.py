#!/usr/bin/env python3

import argparse
import os

# variables defined for coloring printed text
red = '\033[31m'
green = '\033[32m'
blue = '\033[34m'
colorend = '\033[00m'

# Add command line argument flags to get the original and replica parent folder
# paths and get the original and replica folder paths.
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--original', required=True,
		    help='path to the original parent folder')
parser.add_argument('-r', '--replica', required=True,
		    help='path to the replica parent folder')
args = parser.parse_args()

# Recursively iterate through the original folder.
for root, _, files in os.walk(args.original):
  replicaRoot = root.replace(args.original, args.replica, 1)

  # Create the root folder in the replica folder if it doesn't exist.
  if not os.path.isdir(replicaRoot):
    print('\ncreating %s%s%s' % (blue, replicaRoot, colorend))
    try:
      os.mkdir(replicaRoot)
    except OSError:
      print('%scould not create %s%s' % (red, replicaRoot, colorend))
    else:
      print('%ssuccessfully created %s%s' % (green, replicaRoot, colorend))
