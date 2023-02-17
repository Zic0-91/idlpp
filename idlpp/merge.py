# Name: merge.py
# Purpose: Merge Generatated files
# Author: Nicolas Ferrandez <nicolas DOT ferrandez AT free DOT fr>
# Copyright: (c) 2018 Nicolas Ferrandez <nicolas DOT ferrandez AT free DOT fr>
# License: MIT License
#
#######################################################################

from __future__ import unicode_literals

import os
import argparse
from arpeggio import *
from arpeggio import RegExMatch as _

#GRAMMAR
def WS():                  return _(r"(\t|\n|\r| )+")
def START_():              return "//START_"
def START():               return START_, id,
def STOP():                return "//STOP"
def id():                  return _(r"\w+")
def plain_text():          return _(r"((?!//STOP).)*") #Any char but not //STOP
def text():                return [plain_text, WS]

def user_code():           return START, OneOrMore(text), STOP
def expression():          return [user_code, text]

#FILE
def fileGen():            return OneOrMore( expression ),EOF

	

	
#Generic Visitor
class FileVisitor(PTNodeVisitor):

	def __init__(self, debug):
		super(FileVisitor, self).__init__(debug=debug)
		self.symbol_table = {}

	def msg(self, msg):
		if self.debug:
			print(msg)
	
	def log(self, node, children):
		self.msg("NODE.NAME " + node.name) 
		self.msg("NODE.RULE_NAME " + node.rule_name)
		for child in children:
			self.msg("CHILD " + child) 
	
	def addSymbol(self, symbol, contend):
		if symbol in self.symbol_table:
			print(f'ERROR : TAG {symbol} already defined')
			sys.exit(0)
			
		self.msg("ADD SYMBOL : " + symbol)
		self.symbol_table[ symbol ] = contend			

	def isSymbol(self, symbol):
		return (symbol in self.symbol_table)
	
	def getSymbol(self, symbol):
		res = "\n"
		if symbol in self.symbol_table:
			res = self.symbol_table[ symbol ]
		
		return res				

		
class FileExtractor(FileVisitor):

	def __init__(self, debug):
		super(FileExtractor, self).__init__(debug=debug)

	#Visitors
	def visit_user_code(self, node, children):
		self.log(node,children)
		
		if len( children ) > 1:
			self.addSymbol( children[0], "".join( children[1:] ) )

			
	def visit_expression(self, node, children):
		self.log(node,children)
		return "".join(children)

	def visit_fileGen(self, node, children):
		self.log(node,children)
		
		return self.symbol_table		



class FileGenerator(FileVisitor):

	def __init__(self, debug, table):
		super(FileGenerator, self).__init__(debug=debug)
		self.symbol_table = table
			
	#Visitors
	def visit_user_code(self, node, children):
		self.log(node,children)
		
		# IF the symbol, is already defined, 
		# it means that the section was extract from the FileExtractor pass
		# => get the section contend
		if self.isSymbol( children[0] ):
			contend = self.getSymbol( children[0] )
		else:
			contend = "".join( children[1:] )
			self.addSymbol( children[0], contend )
		
		res = "//START_" + children[0] + contend + "//STOP"
			
		return res
	
	def visit_expression(self, node, children):
		self.log(node,children)
		return "".join(children)

	def visit_fileGen(self, node, children):
		self.log(node,children)
		
		return "".join( children )			
		
#MAIN
def Merge(textIn, texteOut, debug=False):

	#Parser instanciation
	parser = ParserPython(fileGen, skipws=False, debug=debug)
	
	TAGS={}
	if texteOut != "":
		#Parse output file to retrieve TAGS
		parse_tree = parser.parse(texteOut)
		Visitor = FileExtractor(debug=debug)
		TAGS = visit_parse_tree(parse_tree, Visitor)
	
	#Parse input
	parse_tree = parser.parse(textIn)
	Visitor = FileGenerator(table=TAGS, debug=debug)
	res = visit_parse_tree(parse_tree, Visitor)
	return res
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='merge')
	parser.add_argument("-d", "--debug", action="store_true", help="enable debugging")
	parser.add_argument("-v", "--version", action="version", version='%(prog)s 1.0 beta')
	parser.add_argument("-o", "--output",  help="output file")
	parser.add_argument("new_file", type=argparse.FileType('r'), help="file to merge")
	parser.add_argument("ref_file", type=argparse.FileType('r'), help="reference file")
	args = parser.parse_args()

	txtRes = Merge( args.new_file.read(), args.ref_file.read(), debug=args.debug)
	args.new_file.close()
	args.ref_file.close()
	
	#Manage output
	if args.output:
		open(args.output, 'w').write( txtRes )
	else:
		print(txtRes)
	
	