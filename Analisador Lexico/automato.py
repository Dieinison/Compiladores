#!/usr/bin/env python
# -*- coding: utf-8 -*-
import alfabeto as alfa

#definicoes
ep = '?'
estadoInicial = 1

alfa3 = [0,1]
afd3 = frozenset([])
afn3 = {
		1: { 0:set([1]) , 1:set([1,2]) }, 
		2: { 0:set([3]) , 1:set([3]) }, 
		3: { 0:set([4]) , 1:set([4]) }, 
		4: { 0:set([5]) , 1:set([5])}, 
		5: { 0:set([6]), 1:set([6])}, 
		6: {} 
		}

#para teste
#alfaTeste = alfa.getAlfaTeste()
afnTeste = {
	0:{ep:set([1,4,6,8])}, 1:{"i":set([2])}, 2:{"f":set([3])}, 3:{},
	4:{'"':set([5]),"'":set([5])}, 5:{"i":set([5]),"f":set([5]),"a":set([5]),"b":set([5]),"'":set([5]), '"':set([5]),
	"0":set([5]),"1":set([5]),"2":set([5])}, 6:{'0':set([7]),'1':set([7]), '2':set([7])}, 7:{"0":set([7]),"1":set([7]),"2":set([7])}, 
	8:{"b":set([9]),"a":set([9]),"i":set([9]),"f":set([9])},
	9:{"b":set([9]), "a":set([9]), "i":set([9]), "f":set([9]), 
	"0":set([9]),"1":set([9]), "2":set([9])}
}

afn = { 0:{ep:set([1,5,12,14,16,19,24,31,38,40,42,44,46,48,50,52,54,56,58,61, 64, 66, 69,72,75,78,15]) },
1:{'i':set([2]) }, 2:{"n":set([3]) }, 3:{"t":set([4])}, 4:{}, 5:{"s":set([6]) }, 6:{"t":set([7]) }, 7:{"r":set([8])}, 
8:{"i":set([9])}, 9:{"n":set([10])}, 10:{"g":set([11])},11:{}, 12:{'"':set([13]), "'":set([13])}, 13:{'a':set([13]),
'b':set([13]), 'c':set([13]), 'd':set([13]), 'e':set([13]), 'f':set([13]), 'g':set([13]), 'h':set([13]),'i':set([13]), 
'j':set([13]), 'k':set([13]), 'l':set([13]), 'm':set([13]), 'n':set([13]), 'o':set([13]),'p':set([13]), 'q':set([13]), 
'r':set([13]), 's':set([13]), 't':set([13]), 'u':set([13]), 'v':set([13]),'w':set([13]), 'x':set([13]), 'y':set([13]), 
'z':set([13]), 'A':set([13]),'B':set([13]), 'C':set([13]), 'D':set([13]), 'E':set([13]), 'F':set([13]), 'G':set([13]), 
'H':set([13]),'I':set([13]), 'J':set([13]), 'K':set([13]), 'L':set([13]), 'M':set([13]), 'N':set([13]), 'O':set([13]),
'P':set([13]), 'Q':set([13]), 'R':set([13]), 'S':set([13]), 'T':set([13]), 'U':set([13]), 'V':set([13]),'W':set([13]), 
'X':set([13]), 'Y':set([13]), 'Z':set([13]), '_':set([13]), '+':set([13]), '-':set([13]), '*':set([13]), '/':set([13]), 
'%':set([13]), '=':set([13]), '!':set([13]), '<':set([13]), '>':set([13]), '&':set([13]), '|':set([13]),',':set([13]), 
';':set([13]), '[':set([13]), ']':set([13]), '(':set([13]), ')':set([13]), '{':set([13]), '}':set([13]), '?':set([13]), 
"'":set([13]), ':':set([13]), '@':set([13]), '\\':set([13]), '.':set([13]), '"':set([13])}, 
14:{'0':set([15]), '1':set([15]), '2':set([15]), '3':set([15]), '4':set([15]), '5':set([15]), '6':set([15]), 
'7':set([15]), '8':set([15]), '9':set([15]) }, 15:{'0':set([15]), '1':set([15]), '2':set([15]), '3':set([15]), 
'4':set([15]), '5':set([15]), '6':set([15]), '7':set([15]), '8':set([15]), '9':set([15]) },
16:{"i":set([17])}, 17:{"f":set([18])}, 18:{}, 19:{"e":set([20])}, 20:{"l":set([21])}, 21:{"s":set([22])}, 22:{"e":set([23])},
23:{}, 24:{"r":set([25])}, 25:{"e":set([26])}, 26:{"t":set([27])}, 27:{"u":set([28])}, 28:{"r":set([29])}, 29:{"n":set([30])}, 
30:{}, 31:{"s":set([32])}, 32:{"t":set([33])}, 33:{"a":set([34])}, 34:{"t":set([35])}, 35:{"i":set([36])}, 36:{"c":set([37])}, 
37:{}, 38:{",": set([39])}, 39:{}, 40:{";":set([41])},41:{}, 42:{".":set([43])}, 43:{}, 44:{"(":set([45])}, 45:{}, 46:{")":set([47])},47:{}, 48:{"[":set([49])}, 49:{},
50:{"]":set([51])}, 51:{}, 52:{"{":set([53])}, 53:{}, 54:{"}":set([55])}, 55:{},
56:{'a':set([57]),'b':set([57]), 'c':set([57]), 'd':set([57]), 'e':set([57]), 'f':set([57]), 'g':set([57]), 'h':set([57]),'i':set([57]), 'j':set([57]), 'k':set([57]), 'l':set([57]), 'm':set([57]), 'n':set([57]),
'o':set([57]),'p':set([57]), 'q':set([57]), 'r':set([57]), 's':set([57]), 't':set([57]), 'u':set([57]), 'v':set([57]),
'w':set([57]), 'x':set([57]), 'y':set([57]), 'z':set([57]), 'A':set([57]),'B':set([57]), 'C':set([57]), 'D':set([57]), 
'E':set([57]), 'F':set([57]), 'G':set([57]), 'H':set([57]),'I':set([57]), 'J':set([57]), 'K':set([57]), 'L':set([57]), 
'M':set([57]), 'N':set([57]), 'O':set([57]),'P':set([57]), 'Q':set([57]), 'R':set([57]), 'S':set([57]), 'T':set([57]), 
'U':set([57]), 'V':set([57]),'W':set([57]), 'X':set([57]), 'Y':set([57]), 'Z':set([57]), '_':set([57])},
57:{'a':set([57]),'b':set([57]), 'c':set([57]), 'd':set([57]), 'e':set([57]), 'f':set([57]), 'g':set([57]), 
'h':set([57]),'i':set([57]), 'j':set([57]), 'k':set([57]), 'l':set([57]), 'm':set([57]), 'n':set([57]),
'o':set([57]),'p':set([57]), 'q':set([57]), 'r':set([57]), 's':set([57]), 't':set([57]), 'u':set([57]), 
'v':set([57]),'w':set([57]), 'x':set([57]), 'y':set([57]), 'z':set([57]), 'A':set([57]),'B':set([57]), 'C':set([57]), 
'D':set([57]), 'E':set([57]), 'F':set([57]), 'G':set([57]), 'H':set([57]),'I':set([57]), 'J':set([57]), 'K':set([57]), 
'L':set([57]), 'M':set([57]), 'N':set([57]), 'O':set([57]),'P':set([57]), 'Q':set([57]), 'R':set([57]), 'S':set([57]), 
'T':set([57]), 'U':set([57]), 'V':set([57]),'W':set([57]), 'X':set([57]), 'Y':set([57]), 'Z':set([57]), '_':set([57]), 
'0':set([57]), '1':set([57]), '2':set([57]), '3':set([57]), '4':set([57]), '5':set([57]), '6':set([57]), '7':set([57]), 
'8':set([57]), '9':set([57])}, 58:{"!": set([59])}, 59:{"=":set([60])}, 60:{}, 61:{"=":set([62])}, 62:{"=":set([63])}, 63:{}, 
64:{"%":set([65])}, 65:{}, 66:{"<":set([67]), "<":set([67])}, 67:{"=":set([68])}, 68:{}, 69:{"&":set([70])}, 70:{"&":set([71])}, 71:{}, 
72:{"|":set([73])}, 73:{"|":set([74])}, 74:{}, 75:{"+":set([76]), "-":set([76]), "*":set([76]), "/":set([76])}, 
76:{"=":set([77])}, 77:{}, 78:{"+":set([79])}, 79:{"+":set([80])}, 80:{}, 81:{"-":set([82])}, 82:{"-":set([83])}, 83:{},}


def edge(s, c, afn): #conjunto de estados nfa alcancaveis saindo de s, lendo c
	conjEp = []
	if afn.get(s) != None: #verifica se e um estado valido 
	  if afn.get(s).get(c) != None: #verifica se tem transicoes
	    for i in afn.get(s).get(c): 
	    	conjEp.append(i)
	return conjEp

def e_clousure(T, afn):
	
	if type(T) == int: #se estado = numero
	 	S = [T]
	 	T1 = set([T])
	else:
		S = T #pilha
		T1 = set(T) #e_clousure(T)
	
	while(len(S) != 0): #enquanto pilha nao vazia
		t = S.pop() #pego topo
		t_t = afn.get(t) #dic de transicoes
		if t_t != None: #se tem transacao
			for v in t_t: #percorre transicoes
				if v == '?': #se encontro transicoes epson
					aux = t_t.get(v) #set de estados alcanveis por epson
					if aux != None:
						for u in aux: #para cada estado do conjunto retornado
							if u not in T1: #se nao estiver em e_clousure(T)
								T1 = T1.union([u])
								S.append(u)
	T1 = list(T1) #conversao do set para lista
	return T1

def DFAedge(D, c, afn):
	S = [] #conjunto de estados
	
	if type(D) == int: #verifica tipo do conjunto de estados
		D = [D]
	
	for s in D: #percorre estados
	  fset = edge(s, c, afn) #para cada estado chama o edge
	  if len(fset) > 0: #nao adiciona [] no conjunto de estados
	  	for i in fset: 
	  		S.append(i) #resultado de edge põe em S
	S = e_clousure(S, afn) #chama o clousure para S
	
	return S

def conversor_afd(afn, alfabeto):
	afd = {} #afd que vou retornar
	pilha = [] #pilha de estados
	estadosMarcados = [] #estados já visitados
	pilha.append(e_clousure(estadoInicial, afn))
	
	while(len(pilha) > 0):
		trans = {} #dic de transicoes
		estado = pilha.pop() #estado corrente 
		estadosMarcados.append(estado)

		for a in alfabeto: #para cada simbolo do alfabeto
			u = DFAedge(estado, a, afn)
			if(u not in pilha and len(u) > 0 and u not in estadosMarcados):
				pilha.append(u)
			trans[a] = frozenset(u)
		afd[frozenset(estado)] = trans
	
	return afd

afd3 = conversor_afd(afn3, alfa3)
print afd3