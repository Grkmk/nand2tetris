#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:20:28 2019

@author: gk
"""
import databaseModule
import string

## syntax analyzer
# input  -> all jack files within folder
#           space, newLine & comments are ignored (input)
#           2 major types: terminal & non-terminal
# output -> .xml for each file within folder
#           terminal: <xxx> terminal </xxx>
#                     xxx is one of five lexical tokens
#           non-terminal: <xxx>
#                           recursive code for the body of xxx element
#                         </xxx>
#                         xxx is either one of:
#                           - class, classVarDec, subroutineDec, parameterList, 
#                               subroutineBody, varDec
#                           - statements, whileStatement, ifStatement, returnStatement,
#                               letStatement, doStatement
#                           - expression, term, expressionList

# integer constant -> a decimal number in range 0..32767
# string constant  -> sequence of unicode chars excluding " or \n
# identifier       -> sequence of letters, digits and _, not starting w/ digit

class jackTokenizer:
    def __init__(self, line):
        self.line = line
        self.constructor(line)
   
    def constructor(self, line):
        if line.isspace() or line.strip().startswith('//'): pass
        else:
            if line.find('//') != -1:
                splitLines = line.split('//', 1)
                lineToStrip = splitLines[0]
            else: lineToStrip = line
                    
            outputLine = lineToStrip.strip()
            self.hasMoreTokens(outputLine)
    
    def hasMoreTokens(self, line):
        global tokenTracker, strTracker, token
        tokenTracker, strTracker = 0
        token = ''
        
        for char in line:
            self.advance(char)
    
    def advance(self, char):
        global tokenTracker, strTracker, token
        
        #strConst
        if char == '"':
            if tokenTracker == 1:
                self.tokenType(token)
                tokenTracker = 0
            strTracker += 1
            if strTracker == 2:
                self.tokenType(token)
                strTracker = 0
        elif strTracker == 1: token += char
        
        #space
        elif char == ' ':
            if tokenTracker == 1:
                self.tokenType(token)
                tokenTracker = 0
        
        #symbol
        elif char in databaseModule.symbol:
            if tokenTracker == 1:
                self.tokenType(token)
                tokenTracker = 0
                
            self.tokenType(char)
        
        #token
        else:
            tokenTracker = 1
            token += char

    def tokenType(self, token):
        #identifier
        if token.startswith('"'): self.stringVal(token)
        elif token in databaseModule.symbol: self.symbol(token)
        elif token.startswith(string.digits): self.intVal(token)
        elif token in databaseModule.keyword: self.keyword(token)
        else: self.identifier(token)
    
    def keyword(self, keyword):
        output =  "<keyword>" + keyword + "</keyword>"
        return output
    
    def symbol(self, symbol):
        output = "<symbol>" + symbol + "</symbol>"
        return output
    
    def identifier(self, identifier):
        output = "<identifier>" + identifier + "</identifier>"
        return output
    
    def intVal(self, intVal):
        output = "<integerConstant>" + intVal + "</integerConstant>"
        return output
    
    def stringVal(self, strVal):
        output = "<stringConstant>" + strVal + "</stringConstant>"
        return output
    
 
class compilationEngine:
    def __init__(self, tokenType, tokenValue, inputFile, outputFile):
        self.tokenType = tokenType
        self.tokenValue = tokenValue
        self.outputFile = outputFile
        self.inputFile = inputFile
        self.constructor()
        
    def constructor(self):
        for line in self.inputFile:
            if line.isspace() or line.strip().startswith('//'): continue
            else:
                if line.find('//') != -1:
                    splitLines = line.split('//', 1)
                    lineToStrip = splitLines[0]
                else: lineToStrip = line
                    
                outputLine = lineToStrip.strip()
                self.compileClass(outputLine)
    
    def compileClass(self, line):
        self.outputFile.write("<class>")
        
    
    def compileClassVarDec(self):
        pass
    
    def compileSubroutine(self):
        pass
    
    def compileParameterList(self):
        pass
    
    def compileVarDec(self):
        pass
    
    def compileStatements(self):
        pass
    
    def compileDo(self):
        pass
    
    def compileLet(self):
        pass
    
    def compileWhile(self):
        pass
    
    def compileReturn(self):
        pass
    
    def compileIf(self):
        pass
    
    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass    
