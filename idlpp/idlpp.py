#######################################################################
# Name: idlpp.py
# Purpose: Simple IDL compiler
# Author: Nicolas Ferrandez <nicolas DOT ferrandez AT free DOT fr>
# Copyright: (c) 2018 Nicolas Ferrandez <nicolas DOT ferrandez AT free DOT fr>
# License: MIT License
#
#######################################################################

from __future__ import unicode_literals

import os
import argparse
	
import idlParser
from idlVisitor import * 

	
#MAIN
def main(debug=False):

    # Argument parser
	parser = argparse.ArgumentParser(prog='idlpp')
	parser.add_argument("-d", "--debug",   action='count',              help="enable debugging", default=0)
	parser.add_argument("-v", "--version", action="version",            version='%(prog)s 1.1 beta')
	parser.add_argument("-o", "--output",  type=argparse.FileType('w'), help="output file")
	parser.add_argument("-t", "--types",   action="store_true",         help="enable CPP types/component generators")
	parser.add_argument("file",            type=argparse.FileType('r'), help=".idl file to compile")
	args = parser.parse_args()

	#treate args	
	debug = args.debug	
	print(f'Compiling file {args.file.name}')
	
	#Read input file
	idl_file = args.file.read()

	#Parse IDL File to produce the parse_tree
	parse_tree = idlParser.Parse(idl_file, debug=(debug>=2) )
	
	res = ""
		
	# visit_parse_tree will start semantic analysis.
	# In this case semantic analysis will evaluate expression and
	symbol_table = SymbolTable(debug=(debug>=1))
	
	Visitor = SymbolTableVisitor(debug=(debug>=1))
	symbol_table = Visitor.getSymbolTable()
	res = visit_parse_tree(parse_tree, Visitor)
		
	if args.types:
		Visitor = CppDeclarationVisitor(debug=debug)
		Visitor.setSymbolTable( symbol_table )
		res = visit_parse_tree(parse_tree, Visitor)
	
	#Manage output
	if args.output:
		res = Visitor.finalizeFile( [os.path.basename( args.output.name ), res] )
		args.output.write( res )
	else:
		print(res)

if __name__ == "__main__":
    # In debug mode dot (graphviz) files for parser model
    # and parse tree will be created for visualization.
    # Checkout current folder for .dot files.
    main(debug=True)