#!/usr/bin/env python
# -*- coding: utf-8 -*-

def getNums():
	return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def getLetras():
	return ['a','b','c','d','e','f','g','h', 'i', 'j', 'k','l', 'm', 'n', 'o',
		'p', 'q', 'r','s','t','u','v','w','x','y','z','A','B','C','D','E',
		'F','G','H','I','J','K','L','M','N','O','P','Q','U','V','W','X','Y','Z','_']

def getOperadores():
	return ['+', '-', '*', '/', '%', '=']

def getCaracteresEspeciais():
	return ['!', '<', '>', '&', '|',',', ';', '[', ']', '(', ')', '{', '}']

def getSimbolosEspeciais():
	return ['?', "'", ':', '@', '\\', '.', '"']

def getAlfabeto():
	return getLetras() + getNums() + getOperadores() + getCaracteresEspeciais() + getSimbolosEspeciais()

def getAlfaTeste():
	return ['a','b','i','f','0','1','2'," ' ", ' " ']