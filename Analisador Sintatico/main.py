import sys
from gramatica import *

def analisador_sintatico_novo(GLC, tokens):
	items = GLC.items()
	tabela = GLC.tabelaAnalise()
	listaTokens = tokens.split()
	pilha = [0]
	
	i = 0
	while i < (len(listaTokens)):
		try:
			action = tabela[pilha[-1]][listaTokens[i]] #simbolo topo da pilha
		except KeyError, e:
			print('Erro sintatico -> ' + getErro(listaTokens, i-1)) 
			exit(0)
		slices = action.split()
		if(action == "accept"):
			print("Sucesso")
			break
		elif(action == "reject"):
			print("Erro sintatico")
			break
		
		elif slices[0] == "shift":
			pilha.append(int(slices[1]))# coloca na pilha o indice do item
		
		elif slices[0] == "reduce":
			(X, prod) = GLC.getRegra(int(slices[1])) # pega regra correspondente
			for r in prod.split(): # percorre a regra
				pilha.pop() # remove elementos do topo da pilha
			tmp = tabela[pilha[-1]][X] # se topo da pilha na coluna do nao terminal 
			if tmp != "reject": # for diferente de "reject"
				tmp = tmp.split() # splita, por ex: "shift 4"
				pilha.append(int(tmp[1]))#salva indice do item no topo da pilha
				i -= 1
		elif slices[0] == "aux":
			pilha.append(int(slices[1]))
		i+=1

def getErro(listaTokens, i):
	z = 0
	err = []
	while z < i:
		err.append(listaTokens[z])
		z+=1
	err = list2String(err)
	return err

glc = GLC()

glc.setTerminais([";", "id", ":=", "print", "(", ")", "num", "+", ",", "$"])
glc.setNTerminais(["S", "E", "L"])

glc.addRegra(("S_", "S"))
glc.addRegra(("S", "S ; S"))
glc.addRegra(("S", "id := E"))
glc.addRegra(("S", "print ( L )"))
glc.addRegra(("E", "id"))
glc.addRegra(("E", "num"))
glc.addRegra(("E", "E + E"))
glc.addRegra(("E", "( S , E )"))
glc.addRegra(("L", "E"))
glc.addRegra(("L", "L , E"))

entrada = raw_input()
analisador_sintatico_novo(glc, entrada + ' $')

# def analisador_sintatico(GLC, tokens):
# 	items = GLC.items()
# 	tabela = GLC.tabelaAnaliseNova()
# 	listaTokens = tokens.split()		
# 	pilha = [0]

# 	i = 0
# 	while i < (len(listaTokens)):
# 		action = tabela.get(pilha[-1])
		
# 		if action != None:
# 			action = action.get(listaTokens[i])
# 			if action != None:
# 				slices = action.split()
# 				if(slices[0] == "accept"):
# 					print("Sucesso")
# 					break
# 				elif(slices[0] == "reject"):
# 					print("Erro sintatico")
# 					break
# 				elif slices[0] == "shift":
# 					pilha.append(int(slices[1]))# coloca na pilha o indice do item
# 				elif slices[0] == "reduce":
# 					(X, prod) = GLC.getRegra(int(slices[1])) # pega regra correspondente
# 					for r in prod.split(): # percorre a regra
# 						pilha.pop() # remove elementos do topo da pilha
# 					tmp = tabela[pilha[-1]][X] # se topo da pilha na coluna do nao terminal 
# 					if tmp != "reject": # for diferente de "reject"
# 						temp = temp.split() # splita, por ex: "shift 4"
# 						pilha.append(int(temp[1]))#salva indice do item no topo da pilha
# 						i -= 1
# 				elif slices[0] == "aux":
# 					pilha.append(int(slices[1]))
# 		i+=1