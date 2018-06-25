#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import analisador_lexico as al
import alfabeto as alfa
import automato as a
from semantico import *

#definicoes
afn = a.afn
alfabeto = alfa.getAlfabeto()
afd = a.conversor_afd(afn, alfabeto)
tokens = []
codigo = ""

try: #le arquivo
  f = open(sys.argv[1])
  for line in f:
    line = line.replace('\n',' ')
    codigo += line + ' \n '
except Exception, e:
  print e

#tratamento
codigo = codigo.split(" ") #faz um split por espaco
while '' in codigo: #remove espacos em branco desnecessarios
  codigo.remove('')

tokens = al.analisadorLexico(afd, codigo)

(var, escoposVars, fun, escoposFuns) = symbolTable(tokens)
if (var, escoposVars, fun, escoposFuns) != ([],[],[],[]): 
	if verificaUsoVariaveis(tokens, var, escoposVars, escoposFuns): 
		if verificaUsoFuncoes(tokens, fun, escoposFuns, var, escoposVars): 
			if verificaAtribuicoes(tokens, var, escoposVars, fun, escoposFuns): 
				if verificaRetornosFuncoes(tokens, var, escoposVars, fun, escoposFuns):
	 				print "Sucesso"