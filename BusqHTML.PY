#!/usr/bin/env python
# -*- coding: latin-1 -*-


import sqlite3,config, time
from pylexcom import Partes
#from Paginador import Paginador
from BusqSQL import Buscador


from Indizador import Nombres
PAGINA=2 #devuelve 5 resultados por pagina


HTML_FIN='<p><h3>Se terminaron los resultados</h3></p>'


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
        return '  '.join(l)
               
    def ultima_pagina(self):
        raise ("Ultima pagina")
    def primera_pagina(self):
        raise ("Primera pagina")
       
    def corre(self):
        key=0
        for elto in range(13):
            key+=1
            yield key,"{%d}" % elto


class DevuelvoConsulta(Generador):
    '''esta clase usa la anterior para encontrar los sujetos,
    y después muestra en formato html los resultados'''
    HTML_Sujeto='''<h3>%(apel)s, %(nomb)s <i>%(nom2)s</i></h3><br>'''
    HTML_Dato='''<i>%s</i>:%s<br>'''
    HTML_Expte='''<b>%(exp0)s %(cara)s S/%(tipoproc)s</b><br>
        %(fiscalia)s <i>(%(caracter)s)</i><br>'''
    
    def __init__(self,argumento):
        self.tabla=Partes.Sujetos(config.PATH_LEX)
        self.tabla.order_by('Sujetos')
        self.busq=Buscador()
        self.argumento=argumento
        #Paginador.__init__(self) #manejador del cache
        
    def corre(self):
        '''hago la navegacion en lex para armar los html definitivos
        devuelve uno por justiciable encontrado'''
        n=0
        for resultado in self.busq.corre(self.argumento):
            seek='%08d' % resultado
            self.tabla.tabla.Seek(seek) #¡que feo!

            if seek==self.tabla['SUJE']:
                n+=1
                armado=[]
                armado.append(self.HTML_Sujeto % self.tabla)
                obj=self.tabla.parte()
                for expte in obj:
                    armado.append(self.HTML_Expte % obj)
                armado.append('<br>')
                for campo in self.tabla.campos():
                    if not (campo in ['SUJE','APEL','NOMB','NOM2']) and \
                            self.tabla[campo].strip()>'':
                        armado.append(self.HTML_Dato % (campo, self.tabla[campo]))
                yield n,'\n'.join(armado)
            else:
                yield n,'que paso??? %s!=%s' % (seek,self.tabla['SUJE'])
            
            
    def AbrirDB(self):
        self.busq.db=sqlite3.connect(config.PATH_BD)
    
    def CerrarDB(self):
        self.busq.db.close()

def prueba1():
    b=Buscador()
    pala='RAMIREZ JOSE'
    db=sqlite3.connect(config.BD_TEMP)    
    ini=time.time()    
    print 'intento 1'
    SQL= b.genconsulta(b.pares(pala))
    
    print SQL
    cur=db.cursor()
    cur.execute(SQL)
    lista=[]
    for r in cur:
        lista.append(r[0])
    fin=time.time() - ini
    print lista
    print fin

    db=sqlite3.connect('c:/sujetos3.sqlite')    
    ini=time.time()    
    
if __name__=='__main__':
    pala='RAMIREZ JOSE'
    b=DevuelvoConsulta(pala)

    for r in b.corre():
        print r
        
    
        
