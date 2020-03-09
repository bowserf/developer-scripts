import os
import argparse
from enum import Enum

class RenameAction(Enum):
    upper = 'upper'
    lower = 'lower'
    capitalize = 'capitalize'

def getCapitalizedFilePath(filePath):
    fileName = filePath.split('/')[-1] # -1 is a shortcut ot get the last element
    capitalizedFileName = fileName.capitalize()
    parentPath = os.path.dirname(filePath)
    return parentPath + "/" + capitalizedFileName

def rename_files(path, renameAction):
    isFile = os.path.isfile(path)
    if isFile:
        if renameAction is RenameAction.upper:
            newPath = path.upper()
        elif renameAction is RenameAction.capitalize:
            newPath = getCapitalizedFilePath(path)
        elif renameAction is RenameAction.lower:
            newPath = path.lower()
        else:
            raise Exception('Rename action not managed.')

        os.rename(path, newPath)
        return

    isDirectory = os.path.isdir(path)
    if isDirectory:
        elements = os.listdir(path)
        for element in elements:
            rename_files(path + "/" + element, renameAction)
        return

# parse command line parameters
parser = argparse.ArgumentParser(description='Rename all file names to upper/lower/capitalize case')
# mandatory
parser.add_argument('rename', type=RenameAction, choices=list(RenameAction))
# optional
parser.add_argument('--path', dest='path', nargs='?', default='.')

args = parser.parse_args()

rename_files(args.path, args.rename)