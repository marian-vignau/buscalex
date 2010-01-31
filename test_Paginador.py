#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
El generador es solo una "plantilla", una clase que finalmente
no se usará sino que solo sirve para desarrollo
'''
import unittest
from Paginador import *


class Generador(object):
    RESULTADOS=13
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
               
#    def ultima_pagina(self):
#        return '<p>ultimo resultado</p>'
#    def primera_pagina(self):
#        return '<p>primer resultado</p>'
       
    def corre(self):
        key=0
        for elto in range(self.RESULTADOS):
            key+=1
            yield key,"%d" % elto

class TestNombres(unittest.TestCase):
    def test1(self):
        ge=Generador()    
        g=Paginador(ge)
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
#        g.Marcar(1,1)
#        g.Marcar(2,1)
#        g.Marcar(5,1)
#        print g.Marcado(1,1)
#        print g.Marcado(2,1)
#        f=BusqHTML.Filtrado(g,1)
#        pf=Paginador(f)
#        print pf.PgSiguiente()
#        print pf.PgAnterior()
    def test2(self):
        ge=Generador()  
        ge.RESULTADOS=5
        g=Paginador(ge)
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()

    def test3(self):
        ge=Generador()  
        ge.RESULTADOS=0
        g=Paginador(ge)
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgSiguiente(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        print g.PgAnterior(), g.EsPrimeraPg(), g.EsUltimaPg()
        
if __name__ == '__main__':
    unittest.main()