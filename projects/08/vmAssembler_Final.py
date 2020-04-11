#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:39:37 2019

@author: gk
"""

import os
import vmMods
## definitions

## funtions
def parser(file): 
    for nLine in file:
        if nLine.isspace() or nLine.strip().startswith("//"): continue
        else:
            command = vmMods.codeCleaner(nLine)
            output = vmMods.codeWriter(command)
        
        fileOutput.write(output)
        fileOutput.write("\n")


def toInit():
    ## file input
    print("file/directory input: ")
    usrInput = input()
    currentDir = os.getcwd()
    inputFileDirectory = currentDir + usrInput
    global fileOutput
    setSP = "@256\nD=A\n@SP\nM=D\n"
    sysInit = vmMods.codeWriter("call Sys.init 0") + "\n"
    
    if os.path.isfile(inputFileDirectory):
        # file to read
        fileInput = open(inputFileDirectory)
        
        # file to write
        fileName = usrInput.split(".", 1)
        usrOutput = fileName[0] + ".asm"
        outputFileDirectory = currentDir + usrOutput
        fileOutput = open(outputFileDirectory, "w")
        
        # parse file
        fileOutput.write(setSP)
        fileOutput.write(sysInit)
        parser(fileInput)
        
        # close file
        fileInput.close()
        
    elif os.path.isdir(inputFileDirectory):
        # directory list
        directoryList = os.listdir(inputFileDirectory)
        
        # file to write
        outputFile = inputFileDirectory.rsplit("/", 1)
        outputFileName = "/" + outputFile[1] + ".asm"
        outputFileDirectory = inputFileDirectory + outputFileName
        fileOutput = open(outputFileDirectory, "w")
        
        # parse file
        fileOutput.write(setSP)
        fileOutput.write(sysInit)
        for file in directoryList:
            if file.endswith(".vm"):
                iFile = inputFileDirectory + "/" + file
                fileInput = open(iFile)
                parser(fileInput)
                fileInput.close()
                
    else: raise FileNotFoundError

    fileOutput.close()


toInit()