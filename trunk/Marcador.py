#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Idea:
el generador manda resultados, uno tras otro

'''
PAGINA=3 #devuelve 5 resultados por pagina
class Marcador(object):
    MARCAS={
        0:('''<table><tr><td bgcolor="#E0E0E0">
        <a href='enlace_%d'>Agregar para imprimir</a>''',
        '</td></tr></table>'),
        1:('''<table><tr><td bgcolor="#D0C0FF">
        <a href='enlace_%d'>No imprimir</a>''',
        '</td></tr></table>')}
    
    def __init__(self,generador):
        self.generador=generador
        self.armado=[]
        self.marcas=[]
            def agregar(self):
        'agrupa los resultados y los devuelve en grupos'
        n=0
        for resultado in self.generador.corre():
            self.armado.append(resultado)
            self.marcas.append(0)
            n+=1
            if n%PAGINA==0: #PAGINA=resultados por pagina
                yield self.get_html()
                self.armado=[]
                self.marcas=[]
                
        if len(self.armado):
            yield self.get_html()

    def get_html(self):
        'aca devuelvo el html armado, con marcas'
        temp=[]
        n=0
        for marca, contenido in zip(self.marcas,self.armado):
            temp.append(self.MARCAS[marca][0] % n) 
            temp.append(contenido)
            temp.append(self.MARCAS[marca][1]) 
            n+=1
        return '\n\n'.join(temp)
    def get_plano(self):
        '''devuelvo un html armado, 
            pero sin prefijos o sufijos de marca'''
        return '\n\n'.join(self.armado)
        def get_selec(self):
        'devuelvo solo los que estan seleccionados'
        temp=[]
        for marca, contenido in zip(self.marcas,self.armado):
            if marca:
                temp.append(contenido)
        return '\n\n'.join(temp)
    
    def marco_link(self,href):
        'marco o desmarco, cambio de estado de 0 a 1 y viceversa'
        n=int(href.split('_')[1])
        self.marcas[n]=1-self.marcas[n]        return self.get_html()
    
if __name__=='__main__':
    class G(object):
        def corre(self):
            for x in ['tomate','pera','manzana','banana','cereza']:
                yield '<h3>Fruta %s<h3><b>texto adicional</b>' % x
    
    g=G()
    M=Marcador(g)
    print [x for x in g.corre()]
    print '\n\n----\n'.join([x for x in M.agregar()])
    print M.marco_link('enlace_1')
