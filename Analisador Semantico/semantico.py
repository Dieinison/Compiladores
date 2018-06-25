#!/usr/bin/env python
# -*- coding: utf-8 -*-

tipos = ['INT' , 'STRING']
valores = ['STR' , 'NUM']
operadores = ['+', '-', '/', '*']

#funcao que retira os ID's e monta a tabela de símbolos
def symbolTable(tokens):
	variaveis = [] #lista de tuplas, do tipo [({'nome_var':'tipo_var'}, linha)]
	funcoes = [] #lista de triplas, da forma [({nome_fun: tipo_retorno_fun}, linha, {nome_parametro: tipo})]
	linha = 1 #linhas da leitura do código
	escoposVars = [] #pilha de mapas para colocar variaveis e seus respectivos escopos, [{idEscopo: [lista_nome_variaveis]}]
	escoposFuns = [] #pilha de mapas para colocar funcoes e seus respectivos escopos, [{idEscopo: [lista_nome_funcoes]}]
	currentEscopo = 0 #0 é o escopo global, 1 escopo local
	idEscopo = 1 #dermarcar escopos diferentes
	linha = 1 #linha para guardar e verificar o local da declaracao da funcao
	#Monta tabela de variaveis e funcoes
	for i in range(len(tokens)):
		if tokens[i] == 'ERRO': # significa "\n", pq nao tratei o '\n' analisador lexico
			linha += 1 #nova linha
		if tokens[i] == 'LCBR': #novo escopo
			currentEscopo += 1
		elif tokens[i] == 'RCBR': #fim do escopo
			currentEscopo -= 1 #decrementa 
			idEscopo += 1

		#no caso do id ser variavel
		if (tokens[i] in tipos) and (tokens[i+1][:2] == 'ID') and (tokens[i+2][:4] != 'LPAR') and (tokens[i+2] != 'COMMA') and (tokens[i+2] != 'RPAR'):
			if((idNoEscopo(tokens[i+1][3:-1], linha, str(currentEscopo)+str(idEscopo), variaveis, escoposVars, funcoes, escoposFuns))): #verifica se variavel nao foi declarada no escopo
				print "Variável '"+tokens[i+1][3:-1]+"' causa ambiguidade!"
				return ([],[],[],[])
			else:#caso variavel nao tenha sido declarada no escopo
				variaveis.append(({tokens[i+1][3:-1]: tokens[i]}, linha)) #({var:tipo}, linha)
				if(currentEscopo == 0): #se o escopo for global
					addNoEscopoVar(tokens[i+1][3:-1], currentEscopo, escoposVars) #nome_var, escopo
				else: #se escopo for local
					addNoEscopoVar(tokens[i+1][3:-1], int(str(currentEscopo)+str(idEscopo)), escoposVars) #nome_var, escopo
		#no caso do id ser funcao
		elif (tokens[i] in tipos) and tokens[i+1][:2] == 'ID' and tokens[i+2] == 'LPAR':
			parametros = pegaParametros(tokens, i+2) 
			if len(parametros) == 2 or len(parametros) == 1 or len(parametros) == 0: #caso tenha 0, 1 ou 2 parametros
				
				if((idNoEscopo(tokens[i+1][3:-1], linha, str(currentEscopo)+str(idEscopo), variaveis, escoposVars, funcoes, escoposFuns) == False)): #verifica se ja foi declarado alguma outra funcao ou var com mesmo nome
					funcoes.append(({tokens[i+1][3:-1]: tokens[i]}, linha, parametros))
					
					if(currentEscopo == 0): #se o escopo for global
						addNoEscopoFun(tokens[i+1][3:-1], currentEscopo, escoposFuns) #nome_fun, escopo
					else: #se escopo for local
						addNoEscopoFun(tokens[i+1][3:-1], int(str(currentEscopo)+str(idEscopo)), escoposFuns) #nome_fun, escopo
					
					if len(parametros) == 1: #se tiver 1 parametros, põe no mesmo escopo da funcao
						t = parametros.keys() # pega o parametro
						variaveis.append(({tokens[i+4][3:-1]: tokens[i+3]}, linha))
						addNoEscopoVar(t[0], int(str(currentEscopo+1)+str(idEscopo)), escoposVars) #põe no escopo da funcao
					
					if (len(parametros) == 2): #se tiver 2 parametros, põe no mesmo escopo da funcao
						t = parametros.keys() # pega o parametro
						addNoEscopoVar(t[0], int(str(currentEscopo+1)+str(idEscopo)), escoposVars) #põe no escopo da funcao
						variaveis.append(({tokens[i+4][3:-1]: tokens[i+3]}, linha))
						addNoEscopoVar(t[1], int(str(currentEscopo+1)+str(idEscopo)), escoposVars) #põe no escopo da funcao
						variaveis.append(({tokens[i+7][3:-1]: tokens[i+6]}, linha))
				else:
					print "Funcao '"+tokens[i+1][3:-1]+"' causa ambiguidade!"
					return ([],[],[],[])
			else: #qualquer outra quantidade de parametros
				print "Quantidade de parametros inválida!"
				return([],[],[],[])
	
	return (variaveis, escoposVars, funcoes, escoposFuns)

#pega parametros e guarda em um mapa			
def pegaParametros(tokens, pos):
	count = 0
	parametros = {}
	while tokens[pos] != 'RPAR':
		if (tokens[pos] in tipos):
			parametros[tokens[pos+1][3:-1]] = tokens[pos]
		pos += 1
	return parametros

#verifico se variavel ou funcao ja foi declarada com o mesmo nome no escopo
def idNoEscopo(nome_id, linha, escopoAtual, variaveis, escoposVars, funcoes, escoposFuns):
	#conversao
	if escopoAtual[0] == 0:
		escopoAtual = 0
	else:
		escopoAtual = int(escopoAtual)

	funDefNoEscopo = getFuncoesEscopo(escopoAtual, escoposFuns)
	varDefNoEscopo = getVariaveisEscopo(escopoAtual, escoposVars)

	for (v, l) in variaveis:
		if(v.has_key(nome_id) and l <= linha) and v in varDefNoEscopo:
			return True #tem variável que foi declarada no escopo
	for (f, linha, params) in funcoes:
		if(f.has_key(nome_id) and l <= linha) and f in funDefNoEscopo:
			return True #tem funcao que foi declarada no escopo

	return False #não tem variável declarada no escopo

def idNoEscopoGlobal(nome_id, escoposVars, escoposFuns):
	funDefNoEscopoGlobal = getFuncoesEscopo(0, escoposFuns)
	varDefNoEscopoGlobal = getVariaveisEscopo(0, escoposVars)
	if nome_id in funDefNoEscopoGlobal or nome_id in varDefNoEscopoGlobal:
		return True
	else:
		return False #não tem variável declarada no escopo global
	
#pega funcoes definidas no escopo
def getFuncoesEscopo(escopo, escoposFuns):
	retorno = []
	for i in range(len(escoposFuns)):
		if escoposFuns[i].has_key(escopo): #se encontrou o escopo
			retorno = escoposFuns[i].get(escopo)
			break
	return retorno

#pega variaveis definidas no escopo
def getVariaveisEscopo(escopo, escoposVars):
	retorno = []
	for i in range(len(escoposVars)):
		if escoposVars[i].has_key(escopo): #se encontrou o escopo
			retorno = escoposVars[i].get(escopo)
			break
	return retorno
	
#adiono var ou fun na sua respectiva escopo
def addNoEscopoVar(nome_id, id_escopo, escoposVars):
	escope = []
	for i in range(len(escoposVars)): #percorre escopos de variaveis
		if escoposVars[i].has_key(id_escopo): #caso o escopo exista na tabela
			escope = escoposVars[i].get(id_escopo)#lista de variaveis definidas no escopo
			escope.append(nome_id) # adiciona variavel na lista
			escoposVars[i] = {id_escopo: escope} # atualiza lista de variaveis daquele escopo
			break
	if escope == []: #caso nao encontra escopo declarado, cria novo
		escoposVars.append({id_escopo: [nome_id]})
		
def addNoEscopoFun(nome_id, id_escopo, escoposFuns):
	escope = []
	for i in range(len(escoposFuns)): #percorre escopos de funcoes
			if escoposFuns[i].has_key(id_escopo): #caso o escopo exista na tabela
				escope = escoposFuns[i].get(id_escopo)
				escope.append(nome_id) # adiciona funcao na lista
				escoposFuns[i] = {id_escopo: escope} # atualiza lista de variaveis naquele escopo
				break
	if escope == []:
		escoposFuns.append({id_escopo: [nome_id]})

#verifica se variavel usada foi definida
def verificaUsoVariaveis(tokens, variaveis, escoposVars, escoposFuns):
	currentEscopo = 0 #0 é o escopo global, 1 escopo local
	idEscopo = 1 #dermarcar escopos diferentes
	linha = 1
	for i in range(len(tokens)):
		if tokens[i] == 'ERRO': # significa "\n", pq nao tratei o '\n' analisador lexico
			linha += 1 #nova linha
		if tokens[i] == 'LCBR': #novo escopo
			currentEscopo += 1
		elif tokens[i] == 'RCBR': #fim do escopo
			currentEscopo -= 1 #decrementa 
			idEscopo += 1
		
		if( (tokens[i][:2] == 'ID') and (tokens[i-1] not in tipos) and (tokens[i+1] != 'LPAR') ):
			if not(checkVarDefinida(tokens[i][3:-1], (str(currentEscopo)+str(idEscopo)), variaveis, escoposVars) or idNoEscopoGlobal(tokens[i][3:-1], escoposVars, escoposFuns)):
				print "Variável '"+tokens[i][3:-1]+"' não declarada nesse escopo"
				return False
	return True

def checkVarDefinida(var, escopo, variaveis, escoposVars):
	#conversao
	if escopo[0] == 0:
		escopo = 0
	else:
		escopo = int(escopo)
	
	for i in range(len(variaveis)): 
		if variaveis[i][0].has_key(var): #variável foi definida
			for j in range(len(escoposVars)):
				if escoposVars[j].has_key(escopo):
					if var in escoposVars[j][escopo]: #lista de variaveis definidas naquele escopo
						return True
	return False

#verifica se funcao usada foi definida
def verificaUsoFuncoes(tokens, funcoes, escoposFuns, variaveis, escoposVars):
	currentEscopo = 0 #0 é o escopo global, 1 escopo local
	idEscopo = 1 #dermarcar escopos diferentes
	linha = 1
	for i in range(len(tokens)):
		if tokens[i] == 'ERRO': # significa "\n", pq nao tratei o '\n' analisador lexico
			linha += 1 #nova linha
		if tokens[i] == 'LCBR': #novo escopo
			currentEscopo += 1
		elif tokens[i] == 'RCBR': #fim do escopo
			currentEscopo -= 1 #decrementa 
			idEscopo += 1
		
		#uso de funcao	
		if (tokens[i][:2] == 'ID') and (tokens[i-1] not in tipos) and (tokens[i+1] == 'LPAR'):
			#parametro apenas com um valor
			if tokens[i+2] in valores and tokens[i+3] != 'COMMA':
				params = []
				tipoP = ''
				if tokens[i+2] == 'STR':
					tipoP = 'STRING'
				elif tokens[i+2] == 'NUM':
					tipoP = 'INT'
				params.append(tipoP)
				func = checkFunDefinida(tokens[i][3:-1], str(currentEscopo)+str(idEscopo), funcoes, escoposFuns, params, linha)
				if not func:
					print "Função '"+tokens[i][3:-1]+"' não definida"
					return False
			#dois parametros valores
			elif tokens[i+2] in valores and tokens[i+3] == 'COMMA' and tokens[i+4] in valores:
				params = []
				tipoP1 = ''
				tipoP2 = ''
				if tokens[i+2] == 'STR':
					tipoP1 = 'STRING'
				else:
					tipoP1 = 'INT'
				params.append(tipoP1)
				if tokens[i+4] == 'STR':
					tipoP2 = 'STRING'
				else:
					tipoP2 = 'INT'
				params.append(tipoP2)
				func = checkFunDefinida(tokens[i][3:-1], str(currentEscopo)+str(idEscopo), funcoes, escoposFuns, params, linha)
				if not func:
					print "Função '"+tokens[i][3:-1]+"' não definida"
					return False
			#funcao com um parametro ID
			elif tokens[i+2][:2] == 'ID' and tokens[i+3] != 'COMMA':
				params = []
				tipoP1 = pegaTipoVar(tokens[i+2][3:-1], str(currentEscopo)+str(idEscopo), variaveis, escoposVars)
				params.append(tipoP1)
				func = checkFunDefinida(tokens[i][3:-1], str(currentEscopo)+str(idEscopo), funcoes, escoposFuns, params, linha)
				if not func:
					print "Função '"+tokens[i][3:-1]+"' não definida"
					return False
			#funcoes comparametros ID e valor
			elif tokens[i+2][:2] == 'ID' and tokens[i+3] == 'COMMA' and (tokens[i+4] in valores):
				params = []
				tipoP1 = pegaTipoVar(tokens[i+2][3:-1], str(currentEscopo)+str(idEscopo), variaveis, escoposVars)
				params.append(tipoP1)
				if tokens[i+4] == 'STR':
					tipoP2 = 'STRING'
				else:
					tipoP2 = 'INT'
				params.append(tipoP2)
				func = checkFunDefinida(tokens[i][3:-1], str(currentEscopo)+str(idEscopo), funcoes, escoposFuns, params, linha)
				if not func:
					print "Função '"+tokens[i][3:-1]+"' não definida"
					return False
			#funcoes comparametros valor e ID
			elif tokens[i+2] in valores and tokens[i+3] == 'COMMA' and tokens[i+4][:2] == 'ID':
				params = []
				if tokens[i+2] == 'STR':
					tipoP1 = 'STRING'
				else:
					tipoP1 = 'INT'
				params.append(tipoP1)
				tipoP2 = pegaTipoVar(tokens[i+4][3:-1], str(currentEscopo)+str(idEscopo), variaveis, escoposVars)
				params.append(tipoP2)
				func = checkFunDefinida(tokens[i][3:-1], str(currentEscopo)+str(idEscopo), funcoes, escoposFuns, params, linha)
				if not func:
					print "Função '"+tokens[i][3:-1]+"' não definida"
					return False
			#funcoes com dois parametros IDs
			elif tokens[i+2][:2] == 'ID' and tokens[i+3] == 'COMMA' and tokens[i+4][:2] == 'ID':
				params = []
				tipoP1 = pegaTipoVar(tokens[i+2][3:-1], str(currentEscopo)+str(idEscopo), variaveis, escoposVars)
				params.append(tipoP1)
				tipoP2 = pegaTipoVar(tokens[i+4][3:-1], str(currentEscopo)+str(idEscopo), variaveis, escoposVars)
				params.append(tipoP2)
				func = checkFunDefinida(tokens[i][3:-1], str(currentEscopo)+str(idEscopo), funcoes, escoposFuns, params, linha)
				if not func:
					print "Função '"+tokens[i][3:-1]+"' não definida"
					return False
	return True

def checkFunDefinida(fun, escopo, funcoes, escoposFuns, params, linha):
	#conversao
	if escopo[0] == 0:
		escopo = 0
	else:
		escopo = int(escopo)

	for i in range(len(funcoes)):
		if funcoes[i][0].has_key(fun):#funcao foi definida
			if verificaParametros(params, funcoes[i][2]) and funcoes[i][1] <= linha: #verifica se funcao foi declarada antes do uso 
				return True
	return False

#verifica quantidade e tipos de parametros
def verificaParametros(params, paramsDaFuncao):
	if len(params) != len(paramsDaFuncao):
		return False
	else:
		temp = paramsDaFuncao.values()
		for i in range(len(paramsDaFuncao)):
			if params[i] != temp[i]:
				print "Tipo '"+ " ".join(str(p) for p in params) +"' do(s) parametro(s) não compatível com a definicao da funcao"
				return False
		return True 

def pegaTipoVar(var, escopo, variaveis, escoposVars):
	#conversao
	if escopo[0] == 0:
		escopo = 0
	else:
		escopo = int(escopo)
	
	esc = []
	for j in range(len(escoposVars)):
		if escoposVars[j].has_key(escopo):
			esc = escoposVars[j].get(escopo) #lista de variaveis no escopo
	
	# se não encontrou no escopo local, procura no global
	if var not in esc or esc == []:
		esc = getVariaveisEscopo(0, escoposVars)
	
	for i in range(len(variaveis)):
		if variaveis[i][0].has_key(var) and var in esc:
			return variaveis[i][0].get(var) #retorna tipo da variavel
	return " "

def pegaTipoFun(fun, escopo, funcoes, escoposFuns):
	#conversao
	if escopo[0] == 0:
		escopo = 0
	else:
		escopo = int(escopo)
	
	esc = []
	for j in range(len(escoposFuns)):
		if escoposFuns[j].has_key(escopo):
			esc = escoposVars[j].get(escopo) #lista de funcoes no escopo

	# se não encontrou no escopo local, procura no global
	if fun not in esc or esc == []:
		esc = getFuncoesEscopo(0, escoposFuns)

	for i in range(len(funcoes)):
		if funcoes[i][0].has_key(fun) and fun in esc:
			return funcoes[i][0].get(fun) #retorna tipo da funcao
	return " "

#verifica as atribuições
def verificaAtribuicoes(tokens, var, escoposVars, fun, escoposFuns):
	currentEscopo = 0 #0 é o escopo global, 1 escopo local
	idEscopo = 1 #dermarcar escopos diferentes
	linha = 1
	for i in range(len(tokens)):
		if tokens[i] == 'ERRO': # significa "\n", pq nao tratei o '\n' analisador lexico
			linha += 1 #nova linha
		if tokens[i] == 'LCBR': #novo escopo
			currentEscopo += 1
		elif tokens[i] == 'RCBR': #fim do escopo
			currentEscopo -= 1 #decrementa 
			idEscopo += 1

		if tokens[i][:2] == 'ID' and tokens[i+1] == 'OPBI(=)':
			tipo = pegaTipoVar(tokens[i][3:-1], str(currentEscopo)+str(idEscopo), var, escoposVars)
			if tipo != pegaTipoTrechoCodigo(tokens[i+2:], str(currentEscopo)+str(idEscopo), var, escoposVars, fun, escoposFuns, 'SEMI') or tokens[i][3:-1] == tokens[i+2][3:-1]: #não pode ser assign a ela msm
				print "Valor atribuido a variável '"+ tokens[i][3:-1] +"' não é válido."
				return False
	return True

#Funcao que pega o tipo de um dado trecho de codigo, que pode envolver chamadas e retornos de funcoes
#Ela vai de um token corrente ate um " ; "
def pegaTipoTrechoCodigo(tokens, currentEscopo, variaveis, escoposVars, funcoes, escoposFuns, tokenParada):
	tipo = " " #guarda tipo da trecho de código, caso vazio é pq tipo da expressão é inválido
	i = 0
	while i < len(tokens):
		
		if tokens[i] == "STR":
			if tipo == "INT": #se encontrar um tipo, diferente de algum já verificado
				return " " #retorna nada
			tipo = "STRING"
		
		elif tokens[i] == "NUM": #se encontrar um tipo, diferente de algum já verificado
			if tipo == "STRING":
				return " " #retorna nada
			tipo = "INT"
		
		#se for variavel ou funcao
		elif tokens[i][:2] == 'ID':

			if tokens[i+1] != 'LPAR': #se for variavel
				temp = pegaTipoVar(tokens[i][3:-1], currentEscopo, variaveis, escoposVars)
			
			elif(tokens[i+1] == 'LPAR'): #se for funcao
				temp = pegaTipoFun(tokens[i][3:-1], currentEscopo, funcoes, escoposFuns)
				while(tokens[i] != 'RPAR'): #ignora parâmetros
					i += 1
			
			if (temp != tipo and tipo != " "):#diferente do valor previo
				return " "
			else:
				tipo = temp
		
		#se tiver um operador
		elif tokens[i][:5] == "OPBI" and tokens[i][6] not in operadores and tipo == "STRING":
			return " "

		#para quando no ";"
		elif tokens[i] == tokenParada:
			break
		i += 1
	return tipo

def verificaRetornosFuncoes(tokens, var, escoposVars, fun, escoposFuns):
	currentEscopo = 0 #0 é o escopo global, 1 escopo local
	idEscopo = 1 #dermarcar escopos diferentes
	linha = 1
	for i in range(len(tokens)):
		#para cada funcao
		if tokens[i] in tipos and tokens[i+1][:2] == 'ID' and tokens[i+2] == 'LPAR':
			tipoFuncao = tokens[i]
			escopoFuncao = 0
			j = i+3
			
			while True:
				if tokens[i] == 'ERRO': # significa "\n", pq nao tratei o '\n' analisador lexico
					linha += 1 #nova linha
				if tokens[j] == 'LCBR': #novo escopo
					currentEscopo += 1
					escopoFuncao += 1
				elif tokens[j] == 'RCBR': #fim do escopo
					currentEscopo -= 1 #decrementa 
					idEscopo += 1
					escopoFuncao -= 1
					if escopoFuncao == 0:
						break
				
				if tokens[j] == 'RETURN' and escopoFuncao >= 1:
					if tipoFuncao != pegaTipoTrechoCodigo(tokens[j+1:], str(currentEscopo)+str(idEscopo), var, escoposVars, fun, escoposFuns, 'SEMI'):
						print "Tipo de retorno inválido"
						return False
				j += 1
	return True