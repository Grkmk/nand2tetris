#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:49:03 2019

@author: gk
"""

import tokenCompile
import os

### jackAnalyzer
## jackTokenizer
## compilationEngine
## symbolTable (next chp.)
## vmCodeWriter (next chp.)

### jackAnalyzer
# create a jackTokenizer from .jack input file
# create an .xml output file and prepare to write
# use compilationEngine to read & write

def toInit():
    ## file input
    print("file/directory input: ")
    usrInput = input()
    currentDir = os.getcwd()
    inputFileDirectory = currentDir + usrInput
    global fileOutput
    
    if os.path.isfile(inputFileDirectory):
        # file to read
        fileInput = open(inputFileDirectory)
        
        # file to write
        fileName = usrInput.split(".", 1)
        usrOutput = fileName[0] + ".xml"
        outputFileDirectory = currentDir + usrOutput
        fileOutput = open(outputFileDirectory, "w")
        
        # tokenize & compile file
        tokenCompile.jackTokenizer(fileInput, fileOutput)
        
        # close file
        fileInput.close()
        fileOutput.close()
        
    elif os.path.isdir(inputFileDirectory):
        # directory list
        directoryList = os.listdir(inputFileDirectory)
        
        # tokenize & compile file
        for file in directoryList:
            if file.endswith(".jack"):
                
                # file to read
                iFile = inputFileDirectory + "/" + file
                fileInput = open(iFile)
                
                # file to write
                outputFileName = "/" + file + ".xml"        
                outputFileDirectory = inputFileDirectory + outputFileName
                fileOutput = open(outputFileDirectory, "w")
                
                # tokenize & compile
                tokenCompile.jackTokenizer(fileInput, fileOutput)
                
                # close file
                fileInput.close()
                fileOutput.close()
                
    else: raise FileNotFoundError


toInit()

































