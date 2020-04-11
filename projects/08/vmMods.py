#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 16:26:22 2019

@author: gk
"""

## definitions

# writeArithmetic definitions
gtOpTracker = 0
ltOpTracker = 0
eqOpTracker = 0

# codeWriter definitions
arithmeticList = ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")
labelIfGoto = ("label", "if-goto", "goto")
functionCallReturn = ("function", "call", "return")
pushPop = ("push", "pop")

# writeFunctionCallReturn definitions
returnInput = "@LCL\nD=M\n@R13\nM=D\n@5\nD=A\n@R13\nA=M-D\nD=M\n@R14\nM=D\n@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n@R13\nA=M-1\nD=M\n@THAT\nM=D\n@2\nD=A\n@R13\nA=M-D\nD=M\n@THIS\nM=D\n@3\nD=A\n@R13\nA=M-D\nD=M\n@ARG\nM=D\n@4\nD=A\n@R13\nA=M-D\nD=M\n@LCL\nM=D\n@R14\nA=M\n0;JMP"
fVal = 0

## functions

# writeArithmetic -> add // sub // neg // eq // gt // lt // and // or // not    
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
    
    if command == "add": output = addOp
    elif command == "sub": output = subOp
    elif command == "neg": output = negOp
    elif command == "eq":
        output = eqOp
        eqOpTracker += 1
    elif command == "gt":
        output = gtOp
        gtOpTracker += 1
    elif command == "lt":
        output = ltOp
        ltOpTracker += 1
    elif command == "and": output = andOp
    elif command == "or": output = orOp
    else: output = notOp ## command == "not":       
    
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
        if segmentArg == "constant": output = pushConstant
        elif segmentArg == "local": output = pushLocal
        elif segmentArg == "argument": output = pushArgument
        elif segmentArg == "this": output = pushThis
        elif segmentArg == "that": output = pushThat
        elif segmentArg == "static": output = pushStatic
        elif segmentArg == "temp": output = pushTemp
        else:
            if indexArg == "0": output = pushPointer0
            else: output = pushPointer1
    elif pushPopArg == "pop":
        if segmentArg == "local": output = popLocal
        elif segmentArg == "argument": output = popArgument
        elif segmentArg == "this": output = popThis
        elif segmentArg == "that": output = popThat
        elif segmentArg == "static": output = popStatic
        elif segmentArg == "temp": output = popTemp
        else:
            if indexArg == "0": output = popPointer0
            else: output = popPointer1
    else: output = None
    
    return output


def writeLabelIfGoto(command):
    args = command.split()
    arg0 = args[0]
    labelName = args[1]
    ILabel = "(LABEL" + labelName + ")"
    IIfGoto = "@SP\nM=M-1\nA=M\nD=M+1\n@LABEL" + labelName + "\nD;JEQ"
    IGoto = "@LABEL" + labelName + "\n0;JMP"
    
    if arg0.startswith("label"): output = ILabel
    elif arg0.startswith("if-goto"): output = IIfGoto
    elif arg0.startswith("goto"): output = IGoto
    else: output = "\n"
    
    return output


def writeFunctionCallReturn(command):
    args = command.split()
    arg0 = args[0]
    global fVal
    
    if arg0 == "function":
        functionName = args[1]
        lclVars = args[2]
        fnDefInput = ""
        lclVar = int(lclVars)
        fnDef = "(" + functionName + ")"
        while lclVar > 0:
            lclVarInput = "\n@" + str(lclVar) + "\nD=A-1\n@LCL\nA=M+D\nM=0\n@SP\nM=M+1"
            fnDefInput = fnDefInput + lclVarInput
            lclVar -= 1
        output = fnDef + fnDefInput  
    
    elif arg0 == "return": output = returnInput
    
    else: # caller method input
        functionName = args[1]
        ArgVars = args[2]
        fnName = functionName + "Ret" + str(fVal)
        callerInput = "@" + fnName + "\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@5\nD=A\n@" + ArgVars + "\nD=A+D\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@" + functionName + "\n0;JMP\n(" + fnName + ")"
        output = callerInput
        fVal += 1
    
    return output


def codeWriter(command):
    args = command.split()
    arg0 = args[0]
    
    if command in arithmeticList: output = writeArithmetic(command)
    elif arg0 in pushPop: output = writePushPop(command)
    elif arg0 in labelIfGoto: output = writeLabelIfGoto(command)
    elif arg0 in functionCallReturn: output = writeFunctionCallReturn(command)
    else: output = None

    return output


def codeCleaner(line):
    cmment = line.find("//")
    cLine = line.strip()
    
    if cmment != -1:
        cSplit = cLine.split("//", 1)
        codeOutput = cSplit[0].strip()
    else: codeOutput = cLine
        
    return codeOutput

