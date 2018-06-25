#!/usr/bin/env python
# -*- coding: utf-8 -*-

mapaToken = ["ERRO","ERRO","ID","ID","INT","ERRO","ID","ID","ID","ID","ID",
			"STRING", "ERRO", "STR","ERRO","NUM","ERRO","ID","IF","ERRO","ID",
			"ID","ID","ELSE","ERRO","ID","ID","ID","ID","ID","RETURN",
			"ERRO","ID","ID","ID","ID","ID","STATIC","ERRO","COMMA","ERRO",
			"SEMI","ERRO","DOT","ERRO","LPAR","ERRO","RPAR","ERRO","LBR","ERRO",
			"RBR","ERRO","LCBR","ERRO","RCBR","ERRO","ID","ERRO","OPUN","OPBI",
			"ERRO","OPBI","OPBI","ERRO","OPBI","ERRO","OPBI","OPBI","ERRO","ERRO",
			"OPBI","ERRO","ERRO","OPBI","ERRO","OPBI","OPBI","ERRO", "OPBI","OPUN",
			"ERRO","OPBI","OPUN", "NEWLINE","NEWLINE","NEWLINE"]

def transicao(estados, c, afd):
	result = frozenset([])
	transicoes = {}
	for estado in estados:
		for key in afd: #percorre afd olhando  estados que contém o estado
			if estado in key: #se estado esta em conjunto de estados
				transicoes = afd.get(key)
				if transicoes != None: #se o estado é alcancavel
					aux = transicoes.get(c) #pego transicao
					if aux != None: #se tiver transicao
						result = result.union(aux)
	return result

def analisadorLexico(afd, codigo):
	tokens = []
	estadoAtual = frozenset([])
	estadoInicial = frozenset([])
	
	#preciso guardar o estado inicial do meu afd para saber de onde comecar a leitura
	for k in afd:
		if 0 in k:
			estadoInicial = k
	
	for i in range(len(codigo)): #para cada palavra
		palavra = codigo[i]
		token = ""
		
		if palavra[0] == '"' or palavra[0] == "'": #leitura diferente para string
			if palavra[0] == palavra[-1]:#verifica se aspas fecham
				token = "STR"
			else:
				token = "ERRO"
			tokens.append(token)

		else:
			estadoAtual = estadoInicial
			if palavra == "return":
				token = "RETURN"
				tokens.append(token)
			else: 
				#roda a palavra no automato
				for j in range(len(palavra)): #para cada caractere da palavra
					estadoAtual = transicao(estadoAtual, palavra[j], afd)

				if( len(estadoAtual) > 0):
					estadoAtual = list(estadoAtual) #vou converter em uma lista para simular a prioridade
					estadoAtual.sort()
					
					#fazendo o casamento de padrao
					for l in estadoAtual: #percorre conjunto de estados alcancados
						token = mapaToken[l]
						if(token != "ERRO"):#primeiro estado final encontrado, casa o padrao
							break
					if token == 'ID' or token == 'OPBI':
						tokens.append(token+"("+palavra+")" )
					else:
						tokens.append(token)
				else:
					tokens.append("ERRO")

	return tokens