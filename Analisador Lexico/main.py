#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import analisador_lexico as al
import alfabeto as alfa
import automato as a

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
    codigo += line
except Exception, e:
  print e

#tratamento
codigo = codigo.split(" ") #faz um split por espaco
while '' in codigo: #remove espacos em branco desnecessarios
  codigo.remove('')

tokens = al.analisadorLexico(afd, codigo)

for t in tokens:
	print t,