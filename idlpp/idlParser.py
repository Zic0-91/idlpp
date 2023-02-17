# Name: idlParser.py
# Purpose: Simple IDL parser
# Author: Nicolas Ferrandez <nicolas DOT ferrandez AT free DOT fr>
# Copyright: (c) 2018 Nicolas Ferrandez <nicolas DOT ferrandez AT free DOT fr>
# License: MIT License
#
#######################################################################

from __future__ import unicode_literals

import os
from arpeggio import *
from arpeggio import RegExMatch as _

#GRAMMAR
def comment():             return [_("//.*"), _("/\*.*\*/")]
#Symbols
def number():              return _(r"\d+")
def symbol():              return _(r"\w+")
def operator():            return _(r"\+|\-|\*|\/|\=\=")
def qualified_symbol():    return [_(r"(\w|\:\:)+")]

#Preprocessor
def ifndef():              return Kwd("#ifndef"), symbol
def define():              return Kwd("#define"), symbol
def endif():               return Kwd("#endif"), symbol

#includes
def extention():           return [".idl3", ".idl"]
def include_symbol():      return _(r"(\w+)")
def include():             return Kwd("#include"),  "\"", include_symbol, extention, "\""

def preprocessor():        return [ifndef, define, endif, include]

#default types
def void():                return "void"
def boolean():             return "boolean"
def byte():                return "byte"
def short():               return "short"
def long():                return "long"
def float():               return "float"
def longlong():            return "long long"
def longfloat():           return "long float"
def _default_types():      return [void, boolean, short, byte, short, long, float, longlong, longfloat ]

def unsigned():            return "unsigned"
def signed():              return "signed"
def _signe():              return [unsigned, signed]
def defaut_types():        return ZeroOrMore(_signe), _default_types

#Sequence
def sequence():            return Kwd("sequence"), "<", qualified_symbol, ",", number, ">" 


#Type declaration
def type_symbol():          return [defaut_types, sequence, qualified_symbol ]
def typedef_declaration():  return Kwd("typedef"), type_symbol, symbol

#Enum
def enum_literal():         return symbol
def enum_literallist():     return enum_literal, ZeroOrMore(",", enum_literal)
def enum_symbol():          return symbol
def enum_def():             return Kwd("enum"), symbol, "{", enum_literallist, "}" 

#struct
def member():               return type_symbol, symbol, ";"
def struct_symbol():        return symbol
def struct_def():           return Kwd("struct"), struct_symbol, "{", OneOrMore(member), "}"

#union
def union_symbol():         return symbol
def union_case():           return Kwd("case"), enum_literal, ":", type_symbol, symbol, ";"
def union_def():            return Kwd("union"), union_symbol, Kwd("switch"), "(", enum_symbol, ")", "{", OneOrMore( union_case ), "}"

#Function declaration
def parameter():             return type_symbol, ["inout", "in", "out"], symbol
def parameterlist():         return ZeroOrMore(parameter, ZeroOrMore(","))
def function_symbol():       return symbol
def function_def():          return type_symbol, function_symbol, "(", parameterlist, ")"

#Interface
def interface_symbol():      return symbol
def interface_def():         return Kwd("interface"), interface_symbol, "{", OneOrMore(function_def, Kwd(";")), "}" 

#Componenent
def port_symbol():           return symbol
def receptacle_def():        return Kwd("uses"), qualified_symbol, port_symbol
def facet_def():             return Kwd("provides"), qualified_symbol, port_symbol
def port_def():              return [receptacle_def, facet_def]
def component_symbol():      return symbol
def component_def():         return Kwd("component"), component_symbol, "{", OneOrMore(port_def, Kwd(";")), "}"


#module
def module_symbol():         return symbol
def module_def():            return Kwd("module"), module_symbol, "{", OneOrMore(declaration), "}"

#IDL
def declaration():           return [typedef_declaration, enum_def, struct_def, union_def, function_def, interface_def, component_def, module_def], ";"
def idlLanguage():           return ZeroOrMore( preprocessor), OneOrMore(declaration)

	
#MAIN
def Parse(idl_file, debug=False):

	# Parser instantiation. simpleLanguage is the definition of the root rule
	# and comment is a grammar rule for comments.
	parser = ParserPython(idlLanguage, comment, debug=debug)

	parse_tree = parser.parse(idl_file)
	return parse_tree