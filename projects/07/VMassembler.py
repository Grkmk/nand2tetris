#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:39:37 2019

@author: gk
"""

## RAM allocation
    ## virtual: @SP -> RAM[0] // @LCL -> RAM[1] // @ARG -> RAM[2] // @THIS -> RAM[3]
    #           // @THAT -> RAM[4] // temp -> RAM[5-12] // general -> RAM[13-15]
    ## static:  RAM[16-255] (e.g. push static 3 -> @Xxx.3 D=M ..)
    ## stack:   RAM[256-2047]
    ## heap:    RAM[2048-16483]
    
    ## memory access commands
    ## push <segment> <index>
    ## segments
    # argument = None ## dynamic allocation
    # local = None ## dynamic allocation starting at 0
    # static = None ## allocated & shared by all functions in file
    # constant = None ## allocated & seen by all functions in file
    # this = None
    # that = None
    # pointer = None ## can be set to 0 & 1 by any function
    # temp = None ## can be used by any function for any purpose
    
    ## push / pop / label / goto / if / function / return / call

import os
# global definitions
stackStart = 256
stackPointer = 256
staticPointer = 16
vpList = ("SP", "LCL", "ARG", "THIS", "THAT", "SCREEN", "KBD")
signSP = "@SP"
signLCL = "@LCL"
signARG = "@ARG"
signTHIS = "@THIS"
signTHAT = "@THAT"
gtOpTracker = 0
ltOpTracker = 0
eqOpTracker = 0



## writeArithmetic -> add // sub // neg // eq // gt // lt // and // or // not    
def writeArithmetic(command):
    global gtOpTracker, ltOpTracker, eqOpTracker
 
    addOp = "@SP\nA=M-1\nD=M\nA=A-1\nM=M+D\n@SP\nM=M-1"
    subOp = "@SP\nA=M-1\nD=M\nA=A-1\nM=M-D\n@SP\nM=M-1"
    negOp = "@SP\nA=M-1\nM=-M"
    andOp = "@SP\nA=M-1\nD=M\nA=A-1\nM=M&D\n@SP\nM=M-1"
    orOp = "@SP\nA=M-1\nD=M\nA=A-1\nM=M|D\n@SP\nM=M-1"
    notOp = "@SP\nA=M-1\nM=!M"
    eqOp = "@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\nA=A\nM=0\n@EQTRUE" + str(eqOpTracker) + "\nD;JEQ\n@EQEND" + str(eqOpTracker) + "\n0;JMP\n(EQTRUE" + str(eqOpTracker) + ")\n@SP\nA=M-1\nA=A-1\nM=-1\n(EQEND" + str(eqOpTracker) + ")\n@SP\nM=M-1"
    gtOp = "@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\nA=A\nM=0\n@GTTRUE" + str(gtOpTracker) + "\nD;JGT\n@GTEND" + str(gtOpTracker) + "\n0;JMP\n(GTTRUE" + str(gtOpTracker) + ")\n@SP\nA=M-1\nA=A-1\nM=-1\n(GTEND" + str(gtOpTracker) + ")\n@SP\nM=M-1"
    ltOp = "@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\nA=A\nM=0\n@LTTRUE" + str(ltOpTracker) + "\nD;JLT\n@LTEND" + str(ltOpTracker) + "\n0;JMP\n(LTTRUE" + str(ltOpTracker) + ")\n@SP\nA=M-1\nA=A-1\nM=-1\n(LTEND" + str(ltOpTracker) + ")\n@SP\nM=M-1"

    
    if command == "add":
        output = addOp
    elif command == "sub":
        output = subOp
    elif command == "neg":
        output = negOp
    elif command == "eq":
        output = eqOp
        eqOpTracker += 1
    elif command == "gt":
        output = gtOp
        gtOpTracker += 1
    elif command == "lt":
        output = ltOp
        ltOpTracker += 1
    elif command == "and":
        output = andOp
    elif command == "or":
        output = orOp
    else: ## command == "not":
        output = notOp        
    
    return output

## writePushPop -> called if C_PUSH // C_POP
#  arg2        -> string // should be called only if C_PUSH //
#              -> C_POP // C_FUNCTION // C_CALL
#  arg1        -> string // should not be called if C_RETURN
def writePushPop(command):
    args = command.split()
    pushPopArg = args[0]
    segmentArg = args[1]
    indexArg = args[2]
    global stackPointer
    
    pushConstant = "@" + indexArg + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    pushLocal    = "@" + indexArg + "\nD=A\n@LCL\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    pushArgument = "@" + indexArg + "\nD=A\n@ARG\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    pushThis     = "@" + indexArg + "\nD=A\n@THIS\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    pushThat     = "@" + indexArg + "\nD=A\n@THAT\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    pushStatic   = "@" + indexArg + "\nD=A\n@16\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    pushTemp     = "@" + indexArg + "\nD=A\n@5\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    pushPointer0 = "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    pushPointer1 = "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    popLocal     = "@" + indexArg + "\nD=A\n@LCL\nD=M+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D"
    popArgument  = "@" + indexArg + "\nD=A\n@ARG\nD=M+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D"
    popThis      = "@" + indexArg + "\nD=A\n@THIS\nD=M+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D"
    popThat      = "@" + indexArg + "\nD=A\n@THAT\nD=M+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D"
    popStatic    = "@" + indexArg + "\nD=A\n@16\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D"
    popTemp      = "@" + indexArg + "\nD=A\n@5\nD=A+D\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D"
    popPointer0  = "@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D"
    popPointer1  = "@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D"
    
    if pushPopArg == "push":
        stackPointer += 1
        if segmentArg == "constant":
            output = pushConstant
        elif segmentArg == "local":
            output = pushLocal
        elif segmentArg == "argument":
            output = pushArgument
        elif segmentArg == "this":
            output = pushThis
        elif segmentArg == "that":
            output = pushThat
        elif segmentArg == "static":
            output = pushStatic
        elif segmentArg == "temp":
            output = pushTemp
        else:
            if indexArg == "0":
                output = pushPointer0
            else:
                output = pushPointer1
            
    elif pushPopArg == "pop":
        if segmentArg == "local":
            output = popLocal
        elif segmentArg == "argument":
            output = popArgument
        elif segmentArg == "this":
            output = popThis
        elif segmentArg == "that":
            output = popThat
        elif segmentArg == "static":
            output = popStatic
        elif segmentArg == "temp":
            output = popTemp
        else:
            if indexArg == "0":
                output = popPointer0
            else:
                output = popPointer1
    else:
        output = None
    
    return output 

## code writer function
def codeWriter(command):
    arithmeticList = ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")
    
    if command in arithmeticList:
        output = writeArithmetic(command)
    elif command.startswith("push") or command.startswith("pop"):
        output = writePushPop(command)
    else:
        output = None

    return output

## parser helper
def codeCleaner(line):
    cmment = line.find("//")
    cLine = line.strip()
    
    if cmment != -1:
        cSplit = cLine.split("//", 1)
        codeOutput = cSplit[0].strip()
    else:
        codeOutput = cLine
        
    return codeOutput

## parser function
def parser(file):
    ## Constructor
    fileInit = "@" + str(stackStart) + "\nD=A\n@SP\nM=D\n"
    fileOutput.write(fileInit)
    
    ## hasMoreCommands & advance
    for nLine in file:
        if nLine.isspace() or nLine.strip().startswith("//"):
            continue
        else:
            command = codeCleaner(nLine)
            output = codeWriter(command)
        
        fileOutput.write(output)
        fileOutput.write("\n")

# main (init) program
def toInit():
    ## file input
    print("file input: ")
    usrInput = input()
    currentDir = os.getcwd()
    inputFileDirectory = currentDir + usrInput
    fileInput  = open(inputFileDirectory)
    
    ## file output
    fileName = usrInput.split(".", 1)
    usrOutput = fileName[0] + ".asm"
    outputFileDirectory = currentDir + usrOutput
    
    ## open output file
    global fileOutput
    fileOutput = open(outputFileDirectory, "w")
    
    ## parser
    parser(fileInput)
    
    ## close input file
    fileInput.close()
    
    ## close output file
    fileOutput.close()

toInit()