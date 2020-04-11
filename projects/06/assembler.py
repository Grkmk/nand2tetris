#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:39:37 2019

@author: gk
"""

import os

# global definitions
currentDir = os.getcwd()
inputFileDirectory = currentDir + "/rect/Rect.asm"
outputFileDirectory = currentDir + "/rect/Rect.hack"   
variableAddressTracker = 16

# predefined symbols
symbol = {
        "SP"    : "0000000000000000",
        "LCL"   : "0000000000000001",
        "ARG"   : "0000000000000010",
        "THIS"  : "0000000000000011",
        "THAT"  : "0000000000000100",
        "SCREEN": "0100000000000000",
        "KBD"   : "0110000000000000",
        "R0"    : "0000000000000000",
        "R1"    : "0000000000000001",
        "R2"    : "0000000000000010",
        "R3"    : "0000000000000011",
        "R4"    : "0000000000000100",
        "R5"    : "0000000000000101",
        "R6"    : "0000000000000110",
        "R7"    : "0000000000000111",
        "R8"    : "0000000000001000",
        "R9"    : "0000000000001001",
        "R10"   : "0000000000001010",
        "R11"   : "0000000000001011",
        "R12"   : "0000000000001100",
        "R13"   : "0000000000001101",
        "R14"   : "0000000000001110",
        "R15"   : "0000000000001111"
}

# comp -> a c1 c2 c3 c4 c5 c6
comp = {
        "0"  : "0101010",
        "1"  : "0111111",
        "-1" : "0111010",
        "D"  : "0001100",
        "A"  : "0110000",
        "!D" : "0001101",
        "!A" : "0110001",
        "-D" : "0001111",
        "-A" : "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M"  : "1110000",
        "!M" : "1110001",
        "-M" : "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"
}

# dest -> d1 d2 d3
dest = {
        "None": "000",
        "M"   : "001",
        "D"   : "010",
        "MD"  : "011",
        "A"   : "100",
        "AM"  : "101",
        "AD"  : "110",
        "AMD" : "111"
}

# jump -> j1 j2 j3
jump = {
        "None": "000",
        "JGT" : "001",
        "JEQ" : "010",
        "JGE" : "011",
        "JLT" : "100",
        "JNE" : "101",
        "JLE" : "110",
        "JMP" : "111"
}

# convert decimal to binary
def dec2Bin(n):
    intN = int(n)
    convBin = str(bin(intN).replace("0b",""))
    resultBin = convBin.zfill(16)
        
    return resultBin

# evaluate A-instructions
def aInstruction(line):
    addressInput = line[1:].strip()
    
    if addressInput.isnumeric():
        aOutput = dec2Bin(addressInput)
    
    elif addressInput in symbol:
        aOutput = symbol[addressInput]
    
    else:
        global variableAddressTracker
        aOutput = dec2Bin(variableAddressTracker)
        symbol[addressInput] = aOutput
        variableAddressTracker += 1
        
    return aOutput

# evaluate C-instructions
def cInstruction(line):
    if line.find("=") != -1:
        splitEq = line.split("=", 1)
        dVar = dest[splitEq[0].strip()]
        
        if line.find(";") != -1:
            splitSemi = splitEq[1].split(";", 1)
            jVar = jump[splitSemi[1].strip()]
            cVar = comp[splitSemi[0].strip()]
            
        else:
            jVar = jump["None"]
            cVar = comp[splitEq[1].strip()]
        
        cOutput = "111" + cVar + dVar + jVar
        
    elif line.find(";") != -1:
        splitSc = line.split(";", 1)
        dVar = dest["None"]
        cVar = comp[splitSc[0].strip()]
        jVar = jump[splitSc[1].strip()]
        
        cOutput = "111" + cVar + dVar + jVar
        
    return cOutput
        
# evaluate line
def evalLine(line):
    if line[0]=="@": lineOutput = aInstruction(line)
    else: lineOutput = cInstruction(line)
    
    return lineOutput

# assemble line by line to record labels
def labelRun(line, tracker):
        sLine = line.split(")", 1)
        lLine = sLine[0]
        labelInput = lLine[1:]
        symbol[labelInput] = dec2Bin(tracker)

# assemble line by line 
def assembleLine1(fileInput):
    tracker = -1
    
    for nLine in fileInput:
        if nLine.isspace():
            continue
        
        else:
            cLine = nLine.strip()
            cmment = cLine.find("//")
            
            if cmment != -1 and cLine.startswith("//"): continue
            
            elif cLine.startswith("("):
                sLine = cLine.split(")", 1)
                lLine = sLine[0]
                labelInput = lLine[1:]
                
                if labelInput in symbol: continue
            
                else:
                    symbol[labelInput] = dec2Bin(tracker + 1)
                    
            else: tracker += 1

# assemble line by line 
def assembleLine2(fileInput): 
    file = open(inputFileDirectory)
    assembleLine1(file)
    
    for nLine in fileInput:
        if nLine.isspace():
            continue
        
        else:
            cLine = nLine.strip()
            cmment = cLine.find("//")
            
            if cmment != -1 and cLine.startswith("//"): continue
            
            elif cLine.startswith("("): continue
            
            elif cmment != -1:
                cSplit = cLine.split("//", 1)
                fileOutput.write(evalLine(cSplit[0]))
                fileOutput.write("\n")
                
            else:
                fileOutput.write(evalLine(cLine))
                fileOutput.write("\n")
 
# initialize program
def toInit():        
    global fileInput
    fileInput  = open(inputFileDirectory)
    global fileOutput
    fileOutput = open(outputFileDirectory, "w")

    assembleLine2(fileInput)
    fileInput.close()
    fileOutput.close()

toInit()