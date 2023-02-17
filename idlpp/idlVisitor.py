#######################################################################
# Name: idlVisitor.py
# Purpose: Simple IDL visitor
# Author: Nicolas Ferrandez <nicolas DOT ferrandez AT free DOT fr>
# Copyright: (c) 2018 Nicolas Ferrandez <nicolas DOT ferrandez AT free DOT fr>
# License: MIT License
#
#######################################################################


import os
from arpeggio import *
import hashlib

def addIndent(contend):
	contend = '\t' + contend
	return '\n\t'.join( contend.split('\n') )

####
# Visitor
class IdlVisitor(PTNodeVisitor):

	def __init__(self, debug):
		super(IdlVisitor, self).__init__(debug=debug)
		self.symbol_table = SymbolTable(debug) #empty directory
		self.target = ''
		self.template = {} # declare empty dictionary
	
	#Get the correct template
	# Load template on demand (from cache or disk)
	def getTemplate(self, rule):
		if not rule in self.template:
			try:
				self.msg( "Load rule " + rule + " from template folder" )
				current_dir = os.path.dirname(__file__)
				template_fileName = os.path.join(current_dir, 'template', self.target + "_" + rule + ".template")
				template_file = open(template_fileName)
				self.template[ rule ] = template_file.read()
				template_file.close()
			except IOError:
				print( f'MISSING template file for rule : {rule}')
				self.template[ rule ] = "MISSING template file for rule : " + rule	
	
		return self.template[ rule ]
	
	def msg(self, msg):
		if self.debug:
			print(msg)
	
	def log(self, node, children):
		self.msg("NODE.ID " + str(id(node)) ) 
		self.msg("NODE.NAME " + node.name) 
		self.msg("NODE.RULE_NAME " + node.rule_name)
		for child in children:
			if isinstance(child, str):
				self.msg(f'CHILD {child}') 
	
	#Manage symbol table
	def setSymbolTable(self, symbol_table):
		self.symbol_table = symbol_table
		
	def getSymbolTable(self):
		return self.symbol_table

	def calculateHash(self, node):
		symbol_value = self.symbol_table.findByNodeId( id(node) ).value
		return hashlib.sha224( symbol_value.encode() ).hexdigest()
		
	def finalizeFile(self, children):
		TAG="" + children[0] #get filename
		TAG = TAG.replace('.','_')
		TAG= "_" + TAG.upper() + "_"
		data={'file':children[0], 'TAG': TAG, 'contend':children[1], 'id':hashlib.sha224( TAG.encode() ).hexdigest()}
		return self.getTemplate('file').format( **data )

####
# Visitor
class CppDeclarationVisitor(IdlVisitor):

	def __init__(self, debug):
		super(CppDeclarationVisitor, self).__init__(debug=debug)
		self.target = 'cpp_declaration'

	#preprocessor
	def visit_ifndef(self, node, children):
		self.log(node, children)
		return None
		
	def visit_define(self, node, children):
		self.log(node, children)
		return None

	def visit_include(self, node, children):
		self.log(node, children)
		data={'contend':children[0]}
		return self.getTemplate('include').format( **data )
		
	#Visitors
	def visit_qualified_symbol(self, node, children):
		self.log(node,children)
		#TODO extract dependancy
		return children[0]
	
	def visit_sequence(self, node, children):
		self.log(node, children)
		data={'type':children[0], 'size':children[1]}
		return self.getTemplate('sequence').format( **data )
		

	def visit_typedef_declaration(self, node, children):
		self.log(node,children)
		data={'type':children[1], 'contend':children[0]}
		return self.getTemplate('typedef').format( **data )

		
	def visit_enum_literallist(self, node, children):
		self.log(node,children)
		return ",\n".join( children )
	
	def visit_enum_def(self, node, children):
		self.log(node,children)
		data={'type':children[0],  'contend':addIndent( children[1] )}
		return self.getTemplate('enum_def').format( **data )
	
	def visit_member(self, node, children):
		self.log(node,children)
		data={'type':children[0],  'contend':addIndent( children[1] )}
		return self.getTemplate('member').format( **data )
		
	def visit_struct_def(self, node, children):
		self.log(node,children)
		contend = "\n".join( children[1:])
		data={'type':children[0],  'contend':addIndent( contend )}
		return self.getTemplate('struct_def').format( **data )
	
	def visit_union_case(self, node, children):
		self.log(node,children)
		data={'type':children[1],  'contend':addIndent( children[2])}
		return self.getTemplate('member').format( **data )		
		
	def visit_union_def(self, node, children):
		self.log(node,children)
		contend = "\n".join( children[2:])
		data={'type':children[0],  'contend':addIndent( contend )}
		return self.getTemplate('union_def').format( **data )
	
	def visit_parameterlist(self, node, children):
		self.log(node,children)
		return " ".join(children)
		
	def visit_parameter(self, node, children):
		self.log(node,children)
		templateName = 'parameter_' + children[1] + '_def'
		data={'type':children[0], 'contend':children[2]}
		
		return self.getTemplate( templateName ).format(**data)
		
	def visit_function_def(self, node, children):
		self.log(node,children)
		
		contend = "\n".join( children[2:])
		data={'retType':children[0], 'function':children[1], 'contend':contend}
		return self.getTemplate('function_def').format( **data )
		
	def	visit_interface_def(self, node, children):
		self.log(node,children)
		contend = "\n".join( children[1:])
		data={'itf':children[0],  'contend':addIndent( contend )}
		return self.getTemplate('interface_def').format( **data )

#component		
	def visit_facet_def(self, node, children):
		self.log(node,children)
		return [ node.rule_name, children[0], children[1] ]
		
	def visit_receptacle_def(self, node, children):
		self.log(node,children)
		return [ node.rule_name, children[0], children[1] ]
		
	def visit_component_def(self, node, children):
		self.log(node,children)

		lFacetAccessors = [];
		lReceptablesDeclarations= [];
		lReceptablesConnectors= [];
		
		for elem in children :
			#elem 0 : rule_name 'facet_def or recept_def'
			#elem 1 : interface_name
			#elem 2 : portname
			data={'interface':elem[1], 'contend':elem[2]}
			if elem[0] == 'facet_def':
				lFacetAccessors.append( self.getTemplate( 'facet_def_accessor' ).format( **data ) )
			elif elem[0]  == 'receptacle_def':
				lReceptablesDeclarations.append( self.getTemplate( 'receptacle_def_declaration' ).format( **data ) )
				lReceptablesConnectors.append( self.getTemplate( 'receptacle_def_accessor' ).format( **data ) )
		
		data={'component':children[0],
		'facets_accessors':addIndent(  "\n".join(lFacetAccessors) ), 
		'receptables_declarations':addIndent( "\n".join(lReceptablesDeclarations) ),
		'receptacles_connectors':addIndent(  "\n".join(lReceptablesConnectors) ),
		'id': self.calculateHash( node ) }
		
		return self.getTemplate('component_def').format( **data )	

#all		
	def visit_module_def(self, node, children):
		self.log(node,children)
		contend = "\n".join( children[1:])
		
		data={'module':children[0],  'contend':addIndent( contend ), 'id': self.calculateHash( node ) }
		return self.getTemplate('module_def').format( **data )
		
	def visit_idlLanguage(self, node, children):
		self.log(node,children)
		return "\n".join(children)
		

####
# Symbol Table
class Symbol(object):
	def __init__(self, value, node):
		self.value = value # Symbol value
		self.node = node	# Node of the parer tree containning the Symbol
		
class SymbolTable(object):
	def __init__(self, debug=False):
		self.debug = debug
		self.table = {} #empty directory of table[ symbol.value ] = symbol.node
		self.index = {} #empty directory of table[ id ] = symbol.node

	def add(self, symbol):
		if symbol.value in self.table:
			p = self.table[ symbol.value ].position
			print(f'ERROR : Symbol {symbol.value} already defined at position {p}')
			sys.exit(0)
			
		self.msg("ADD SYMBOL : " + symbol.value)
		self.table[ symbol.value ] = symbol.node
	
	def msg(self, msg):
		if self.debug:
			print(msg)	

	def str(self):
		return "\n".join( self.table.keys() )
		
	def buildIndex(self):
		self.index = {}
		for value in self.table:
			node = self.table[ value ]
			self.index[ id(node) ] = node
	
	def findByNodeId(self, id):
		if id in self.index:
			return self.index[ id ]
		else:
			return None
			
	
def unfold( result, symbolList):
	#Cas 1 : symbolList n'est pas une liste
	if isinstance(symbolList, Symbol):
			result.append( symbolList )
	# Cas2 : des listes de Symbol (dans le cas des modules imbrique)
	else:
		#il faut alors deplier la liste
		for symbol in symbolList:
			unfold( result, symbol)

class SymbolTableVisitor(IdlVisitor):

	def __init__(self, debug):
		super(SymbolTableVisitor, self).__init__(debug=debug)
		self.target = 'symbol'
		self.symbol_table = SymbolTable(debug)
		
	#Visitors
	def visit_ifndef(self, node, children):
		self.log(node, children)
		return None
		
	def visit_define(self, node, children):
		self.log(node, children)
		return None
		
	def visit_qualified_symbol(self, node, children):
		self.log(node, children)
		return children[0]
	
	def visit_sequence(self, node, children):
		self.log(node, children)
		return Symbol(children[0], node)

	def visit_typedef_declaration(self, node, children):
		self.log(node,children)
		return Symbol(children[1], node)
	
	def visit_enum_literallist(self, node, children):
		return None
	
	def visit_enum_def(self, node, children):
		self.log(node,children)
		return Symbol(children[0], node)
	
	def visit_member(self, node, children):
		self.log(node,children)
		return None
		
	def visit_struct_def(self, node, children):
		self.log(node,children)
		return Symbol(children[0], node)
	
	def visit_union_case(self, node, children):
		self.log(node,children)
		return None		
		
	def visit_union_def(self, node, children):
		self.log(node,children)
		return Symbol(children[0], node)
	
	def visit_parameterlist(self, node, children):
		self.log(node,children)
		return None
		
	def visit_parameter(self, node, children):
		self.log(node,children)
		return None
		
	def visit_function_def(self, node, children):
		self.log(node,children)
		return Symbol(children[1], node)
	
	def visit_facet_def(self, node, children):
		self.log(node,children)
		return Symbol(children[1], node)
		
	def visit_receptacle_def(self, node, children):
		self.log(node,children)
		return Symbol(children[1], node)
		
	def visit_component_def(self, node, children):
		self.log(node,children)
		return self.visit_module_def(node, children)
		
	def	visit_interface_def(self, node, children):
		self.log(node,children)
		return self.visit_module_def(node, children)

	def visit_module_def(self, node, children):
		self.log(node,children)
		#rend la liste des symbols : module.symbol
		result = []
		tmp = []
		unfold( tmp, children[1:])
		
		result.append( Symbol( children[0], node) )
		for symbol in tmp:
			result.append( Symbol( children[0] + "." + symbol.value, symbol.node) )
		
		return result
		
	def visit_idlLanguage(self, node, children):
		self.log(node,children)
		res = []
		unfold( res, children)
		#ici il y a une liste de module
		for symbol in res:
			self.symbol_table.add( symbol )
		
		self.symbol_table.buildIndex()
		
		return self.symbol_table.str()
		