from copy import copy #funcao para copiar objetos

# ["S",";","S"] -> " S ; S"
def list2String(list):
	result = ""
	for s in list:
		result += (" " + s.strip())
	return result[1:] #isso pra "S ; S", ao inves " S ; S"

class GLC:
	def __init__(self):
		self.__terminais = []
		self.__nterminais = []
		self.__regras = []
		self.__nullables = set([])
	# getters and setters
	def getTerminais(self):
		return self.__terminais

	def getNTerminais(self):
		return self.__nterminais

	def getRegras(self):
		return self.__regras

	def getNullables(self):
		return self.__nullables

	def setTerminais(self, terminais):
		self.__terminais = terminais

	def setNTerminais(self, nterminais):
		self.__nterminais = nterminais

	def setRegras(self, regras):
		self.__regras = regras

	def setNullables(self, nullables):
		self.__nullables = set(nullables)
	# end getters and setters
	
	def getSimbolos(self):
		return self.getNTerminais() + self.getTerminais()
	
	def getRegra(self, id):
		return self.__regras[id]

	def addRegra(self, (nterminal, r)):
		self.__regras.append((nterminal, r))

	def getDerivacoes(self, nterminal):
		result = []
		for (nt, r) in self.__regras:
			if nt == nterminal:
				result.append(r)
		return result
	
	# X e um simbolo da gramatica, terminal ou nao
	def first(self, simbolo):
		if simbolo in self.getTerminais():
			return set([simbolo])

		first = set([])
		for regra in self.getDerivacoes(simbolo): #para todas as derivacoes
			if regra != "":
				Y = regra.split() #pega uma derivacao
				k = len(Y)
				if Y[0] in self.getTerminais():#se first for terminal
					first.add(Y[0]) #add no conjunto e finaliza a leitura da regra
				else: #se for nao terminal
					if Y[0] != simbolo: #nao add a propia regra
						first = first.union(self.first(Y[0]))
					else:
						j=1
						while(j < k):
							first = first.union(self.first(Y[j]))
							if Y[j] not in self.getNullables():
								break
							j += 1
		return first

	def follow(self, A):
		follow = set([]) #conjunto follow
		for (nt, prod) in self.__regras: #para todas as regras
			Y = prod.split()
			k = len(Y)
			for i in range(k):
				if(Y[i] == A and i < k-1):
					follow = follow.union(self.first(Y[i+1])) #Ex: A->aBb, Follow(B) = first(b)
					if(Y[i+1] in self.getNullables()): #Ex: A->aBbC, onde first(b) e nullable, Follow(B) = first(b) U first(C)
						j = i+2
						while j < k:
							follow = follow.union(self.first(Y[j]))
							if (Y[j] not in self.getNullables()):
								break
							j+=1
		return follow

	#essa funcao e utilizada no clousure
	def __first(self, regra):
		Y = regra.split()
		first = set([])
		for y in Y:
			first = first.union(self.first(y))
			if y not in self.getNullables():
				break
		return first
	
	def clousure(self, I):
		while(True):
			J = copy(I)
			for(A, regra, lh) in I: #(nao_terminal, regra, lookahead)
				ger = regra.split('.') # ex: "S.A B" -> ger = ['S', 'A B']
				X = ger[1].strip().split() # regra AB splita e poe em X = ['A', 'B']
				if X != []:
					if X[0] in self.getNTerminais(): #se A for nao_terminal 
						for y in self.getDerivacoes(X[0]): #para cada producao A->y em G'
							for l in self.__first(list2String(X[1:]).strip() + ' ' + lh): #para cada terminal 'l' no first(Bz), onde z e o lookahead
								if l == '': #se first(Bz) for vazio,  
									l = '$' #marco com simbolo final de leitura
								I = I.union(set([(X[0], '.'+y.strip(), l)])) #adiciona a regra [B->.y, l] em I
			if (J == I): #se nada mudou, break
				break
		return I

	def goTo(self, I, X):# I set of items, X is a grammar symbol(terminal or not)
		J = set([])
		for (A, regra, lh) in I:
			ger = regra.split('.')
			Y = ger[1].strip().split()
			if (Y != []) :
				if (Y[0] == X):
					J.add((A, ger[0].strip()+' '+Y[0].strip()+'.'+list2String(Y[1:]).strip(), lh))
		return self.clousure(J)

	def items(self): # items = estado do automato
		C = []
		(S_, prod) = self.__regras[0]
		C.append(self.clousure(set([(S_, '.'+prod.strip(), '$')])))#S'->.S  $
		while True:
			C_ = copy(C) #para verificar se o conjunto muda ou nao
			for item in C:
				for s in self.getSimbolos(): #terminais e nao_terminais
					tmp = self.goTo(item, s) 
					if(tmp != set([]) and tmp not in C):
						C.append(tmp)
			if (C_ == C):
				break
		return C

	def tabelaAnalise(self):
		tabela = []
		C_ = self.items() # colecao de items de G'(gramatica estendida)
		
		#iniciando a tabela
		for i in range(len(C_)):
			tabela.append({})
			for j in self.getSimbolos():
				tabela[i][j] = "reject"

		#montando a tabela
		for item in C_:
			# o estado i do analisador sintatico e construido apartir do i-esimo item
			i = C_.index(item) # posicao da regra no conjunto de regras que compoem um item 
			for (A, regra, lh) in item: #para cada regra do item
				Y = regra.split('.')# regra "S A.B D" -> ["S A", "B D"] 
				B = Y[1].strip().split() #pega regra do lado direito do ponto, ex: ["B", "D"]
				if B != []:
					# se o simbolo corrente for terminal e o conjunto goto pertence 
					# ao conjunto de items, ou seja, se o estado for alcancado
					if B[0] in self.getTerminais() and self.goTo(item, B[0]) in C_:
						j = C_.index(self.goTo(item, B[0])) # pega o indice do resultado do movimento
						tabela[i][B[0]] = "shift " + str(j) # salva na tabela na indice do item, coluna do simbolo terminal
				elif B == [] and A != "S_": #se B == [], significa que o '.' esta no final da leitura da regra
					j = self.__regras.index((A, Y[0].strip()))
					tabela[i][lh] = "reduce " + str(j)
				elif B == [] and A == "S_":
					tabela[i]["$"] = "accept"
				#As funcoes de transicoes para o estado i sao construidas para todos os nao terminais A
				#usando a regra: se GOTO(ITEMi, A) = ITEMj, entao GOTO[i,A] = j
				if self.goTo(item, A) in C_:
					aux = C_.index(self.goTo(item, A))
					tabela[i][A] = "aux "+str(aux)
		return tabela

	# def tabelaAnalise(self):
	# 	tabela = {}
	# 	C_ = self.items() # colecao de items de G'(gramatica estendida)
	# 	# mapa = {0: "reject", {shift: 'j'}}
	# 	#iniciando a tabela
	# 	for a in range(len(C_)):
	# 		#tabela.append({})
	# 		for j in self.getSimbolos():
	# 			tabela[a] = {"": "reject -1"}
	# 	#montando a tabela
	# 	for item in C_:
	# 		# o estado i do analisador sintatico e construido apartir do i-esimo item
	# 		i = C_.index(item) # posicao da regra no conjunto de regras que compoem um item 
	# 		for (A, regra, lh) in item: #para cada regra do item
	# 			Y = regra.split('.')# regra "S A.B D" -> ["S A", "B D"] 
	# 			B = Y[1].strip().split() #pega regra do lado direito do ponto, ex: ["B", "D"]
	# 			if B != []:
	# 				# se o simbolo corrente for terminal e o conjunto goto pertence 
	# 				# ao conjunto de items, ou seja, se o estado for alcancado
	# 				if B[0] in self.getTerminais() and self.goTo(item, B[0]) in C_:
	# 					j = C_.index(self.goTo(item, B[0])) # pega o indice do resultado do movimento
	# 					tabela[i] = { B[0] :"shift "+str(j)}

	# 				elif B == [] and A != "S_": #se B == [], significa que o '.' esta no final da leitura da regra
	# 					j = self.__regras.index((A, Y[0].strip()))
	# 					tabela[j] = { lh :"reduce " + str(j)}
					
	# 				elif B == [] and A == "S_":
	# 					tabela[i] = {"$": "accept"}
	# 				#As funcoes de transicoes para o estado i sao construidas para todos os nao terminais A
	# 				#usando a regra: se GOTO(ITEMi, A) = ITEMj, entao GOTO[i,A] = j
	# 				#g = self.goTo(item, A) 
	# 				#if g in C_:
	# 				#	g = C_.index(g)
	# 				#	tabela[i] = {A :"aux "+str(g)}
	# 	return tabela