#!/usr/bin/env python3

import argparse
import os
import shutil
import filecmp

# variables defined for coloring printed text
red = '\033[31m'
green = '\033[32m'
blue = '\033[34m'
cyan = '\033[36m'
colorend = '\033[00m'

# Add command line argument flags to get the original and replica parent folder
# paths and get the original and replica folder paths.
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--original', required=True,
		    help='path to the original parent folder')
parser.add_argument('-r', '--replica', required=True,
		    help='path to the replica parent folder')
args = parser.parse_args()

def printError(): print(' %s[error]%s' % (red, colorend))

def printSuccess(): print(' %s✓%s' % (green, colorend))

def copyFile(originalFilePath, replicaFilePath, copyingMessage = 'copying to'):
  print('- %s %s%s%s'
        % (copyingMessage, blue, replicaFilePath, colorend), end = '')
  try: shutil.copy2(originalFilePath, replicaFilePath)
  except Exception: printError()
  else: printSuccess()

# Recursively iterate through the original folder.
for root, _, fileNames in os.walk(args.original):
  replicaRoot = root.replace(args.original, args.replica, 1)

  # Create the root folder in the replica folder if it doesn't exist.
  if not os.path.isdir(replicaRoot):
    print('\ncreating %s%s%s' % (cyan, replicaRoot, colorend), end = '')
    try: os.mkdir(replicaRoot)
    except OSError: printError()
    else: printSuccess()
  
  for fileName in fileNames:
    originalFilePath = root + '/' + fileName
    replicaFilePath = replicaRoot + '/' + fileName 

    # Copy the original file to a replica file if the replica file with the 
    # given file name does not exist.
    if not os.path.exists(replicaFilePath):
      copyFile(originalFilePath, replicaFilePath)
    
    # At this point, a file with the same path as the original file in the
    # replica folder exists, so check the contents and update the replica file 
    # if the contents are different.
    else:
      isSame = filecmp.cmp(originalFilePath, replicaFilePath)
      if not isSame: copyFile(originalFilePath, replicaFilePath, 'updating')
