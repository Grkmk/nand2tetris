#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:22:44 2019

@author: gk
"""

import string

## lexical (terminal) elements
keyword = ('class', 'constructor', 'function', 'method', 'field', 'static',
           'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
           'this', 'let', 'do', 'if', 'else', 'while', 'return')

symbol = ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&',
          '|', '<', '>', '=', '~')

# integer constant -> a decimal number in range 0..32767
digitList = list(string.digits)

# string constant  -> sequence of unicode chars excluding " or \n

# identifier       -> sequence of letters, digits and _, not starting w/ digit



## program structure
# class          -> class  className  {  classVarDec*  subroutineDec*  }
# classVarDec    -> static|field  type  varName  ','varName*  ';'
# type           -> int | char | boolean | className
# subroutineDec  -> constructor | function | method  void | type  subroutineName
#                   ( parameterList ) subroutineBody
# parameterList  -> type  VarName  ','type VarName*
# subroutineBody -> {  varDec*  statements }
# varDec         -> var  type  varName  ','varName*  ';'
# className      -> identifier
# subroutineName -> identifier
# varName        -> identifier



## statements
# statements      -> statement*
# statement       -> letStatement | ifStatement | whileStatement | doStatement |
#                    returnStatement
# letStatement    -> let  varName  '['  expression  ']'  '='  expression  ';'
# ifStatement     -> if  '('  expression  ')'  '{'  statements  '}'
#                    else  '{'  statements  '}'
# whileStatement  -> while  '('  expression  ')'  '{'  statements  '}'
# doStatement     -> do  subroutineCall  ';'
# returnStatement -> return  expression  ';'



## expressions
# expression      -> term  op term *
# term            -> integerConstant | stringConstant | keywordConstant | 
#                    varName | varName  '['  expression  ']' | subroutineCall |
#                    '('  expression  ')' | unaryOp term
# subroutineCall  -> subroutineName  '('  expressionsList  ')' | className|varName
#                    '.'  subroutineName  '('  expressionsList  ')'
# expressionsList -> expression  ','expression*
# op              -> '+', '-', '*', '/', '&', '|', '<', '>', '='
opList = ('+', '-', '*', '/', '&', '|', '<', '>', '=')

# unaryOp         -> '-' | '~'
unaryOpList = ('-', '~')

# keywordConstant -> true | false | null | this
keywordConstant = ('true', 'false', 'null', 'this')





