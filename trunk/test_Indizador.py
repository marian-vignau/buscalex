#!/usr/bin/env python
# -*- coding: latin-1 -*-


'''
El generador es solo una "plantilla", una clase que finalmente
no se usará sino que solo sirve para desarrollo
La lógica: 
Página_siguiente: 


'''
import unittest
from Indizador import *

class Generador(object):
        
    def formateo(self,lista):
        '''acá tomo el objeto que está en el cache 
        y lo preparo para mostrar
        Si dice marca, es porque tiene algun filtro'''
        l=[]
        for x in lista:
            if x[0]:
                l.append('*')
            l.append(x[1])
        return ' ; '.join(l)
               
    def ultima_pagina(self):
        raise ("Ultima pagina")
    def primera_pagina(self):
        raise ("Primera pagina")
       
    def corre(self):
        key=0
        for elto in range(13):
            key+=1
            yield key,"{%d}" % elto

class Filtrado(Generador):
    def __init__(self,paginador,marca):
        self.pagi=paginador
        self.marca=marca
        
    def corre(self):
        for key,elto in self.pagi.GeneCache():
            if self.pagi.Marcado(key,self.marca):
                yield key,elto[1]

class TestNombres(unittest.TestCase, Indizador):
    def testPares(self):
        ge=Generador()    
        g=Paginador(ge)
        print g.PgSiguiente()
        print g.PgSiguiente()
        print g.PgSiguiente()
        print g.PgAnterior()
        print g.PgSiguiente()
        print g.PgSiguiente()
        print g.PgAnterior()
        print g.PgAnterior()
        print g.PgAnterior()
        print g.PgAnterior()
        g.Marcar(1,1)
        g.Marcar(2,1)
        g.Marcar(5,1)
        print g.Marcado(1,1)
        print g.Marcado(2,1)
        f=BusqHTML.Filtrado(g,1)
        pf=Paginador(f)
        print pf.PgSiguiente()
        print pf.PgAnterior()
