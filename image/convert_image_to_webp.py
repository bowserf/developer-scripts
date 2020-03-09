import os
import argparse
from enum import Enum
from distutils.spawn import find_executable

class Format(Enum):
    jpeg = 'jpeg'
    png = 'png'

def checkIfCWebPExistInPath():
    if find_executable("cwebp") is None:
        raise Exception("You must have \"cwebp\" tool in your PATH to execute this script." +
            "You can download it at \"https://developers.google.com/speed/webp/download\".")

def parseArguments():
    parser = argparse.ArgumentParser(description='Convert all images of the selected directory to webp with cwebp tool.')
    parser.add_argument('format', type=Format, choices=list(Format))
    parser.add_argument('--path', dest='path', nargs='?', default='.')
    return parser.parse_args()

def getExtension(format):
    if format is Format.jpeg:
        return ".jpg"
    elif format is Format.png:
        return ".png"
    else:
        raise Exception("Image format not managed.")

def convert_jpeg_to_webp(path, format):
    isFile = os.path.isfile(path)
    if isFile:
        extension = getExtension(format)
        if not path.endswith(extension):
            return
        # escap all spaces in the file path
        spaceProtectedPath = path.replace(" ", "\ ")
        # execute the cwebp tool
        command = "cwebp " + spaceProtectedPath + " -o " + spaceProtectedPath.replace(extension, ".webp")
        os.system(command)
        # remove old image
        if extension in path:
            os.remove(path)
        return

    isDirectory = os.path.isdir(path)
    if isDirectory:
        elements = os.listdir(path)
        for element in elements:
            convert_jpeg_to_webp(path + "/" + element, format)
        return

checkIfCWebPExistInPath()
args = parseArguments()
convert_jpeg_to_webp(args.path, args.format)