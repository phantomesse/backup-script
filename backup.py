#!/usr/bin/env python3

import argparse
import os
import shutil
import filecmp

# variables defined for coloring printed text
__red = '\033[31m'
__green = '\033[32m'
__yellow = '\033[33m'
__blue = '\033[34m'
__cyan = '\033[36m'
__colorend = '\033[00m'

def __printError(): print('%s[error]%s' % (__red, __colorend))

def __printSuccess(): print('%s✓%s' % (__green, __colorend))

def __copyFile(
  originalFilePath, replicaFilePath):
  try: shutil.copy2(originalFilePath, replicaFilePath)
  except Exception: __printError()
  else: __printSuccess()

def backup(originalFolderPath, replicaFolderPath):
  nothingChanged = True

  # Recursively iterate through the original folder.
  for root, _, fileNames in os.walk(originalFolderPath):
    replicaRoot = root.replace(originalFolderPath, replicaFolderPath, 1)

    # Create the root folder in the replica folder if it doesn't exist.
    if not os.path.isdir(replicaRoot):
      nothingChanged = False
      print('\ncreating %s%s%s' % (__cyan, replicaRoot, __colorend), end = ' ')
      try: os.mkdir(replicaRoot)
      except OSError: __printError()
      else: __printSuccess()
    
    for fileName in fileNames:
      originalFilePath = root + '/' + fileName
      replicaFilePath = replicaRoot + '/' + fileName 

      # Copy the original file to a replica file if the replica file with the 
      # given file name does not exist.
      if not os.path.exists(replicaFilePath):
        nothingChanged = False
        print('- copying to %s%s%s' % (__blue, replicaFilePath, __colorend),
              end = ' ')
        __copyFile(originalFilePath, replicaFilePath)
        continue
      
      # At this point, a file with the same path as the original file in the
      # replica folder exists, so check the contents and update the replica file 
      # if the contents are different.
      isSame = filecmp.cmp(originalFilePath, replicaFilePath)
      if isSame: continue
      nothingChanged = False
      print('- updating %s%s%s' % (__blue, replicaFilePath, __colorend),
          end = ' ')
      __copyFile(originalFilePath, replicaFilePath)

  if nothingChanged:
    print('%sCongrats! Your replica is already up-to-date!%s'
          % (__green, __colorend))

  # Recursively iterate through the replica folder.
  extraneousFolders = []
  extraneousFiles = []
  for root, _, fileNames in os.walk(replicaFolderPath):
    originalRoot = root.replace(replicaFolderPath, originalFolderPath, 1)

    # Check if this is a folder that is not in the original folder.
    if not os.path.isdir(originalRoot): extraneousFolders.append(root)

    for fileName in fileNames:
      originalFilePath = originalRoot + '/' + fileName
      replicaFilePath = root + '/' + fileName
      if not os.path.exists(originalFilePath):
        extraneousFiles.append(replicaFilePath)
  if len(extraneousFolders) > 0:
    print('%s\nextraneous folders in %s:%s'
          % (__yellow, replicaFolderPath, __colorend))
    for folder in extraneousFolders:
      print('- %s%s%s' % (__cyan, folder, __colorend))
  if len(extraneousFiles) > 0:
    print('%s\nextraneous files in %s:%s'
          % (__yellow, replicaFolderPath, __colorend))
    for fileName in extraneousFiles:
      print('- %s%s%s' % (__blue, fileName, __colorend))

# Add command line argument flags to get the original and replica parent folder
# paths and get the original and replica folder paths.
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--original', required=True,
        help='path to the original parent folder')
parser.add_argument('-r', '--replica', required=True,
        help='path to the replica parent folder')
args = parser.parse_args()

# Execute the backup.
backup(args.original, args.replica)
