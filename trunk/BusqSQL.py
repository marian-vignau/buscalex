#!/usr/bin/env python
# -*- coding: latin-1 -*-

import config,sqlite3
import Indizador

class Buscador(Indizador.Nombres):
    def __init__(self):
        self.db=sqlite3.connect(config.PATH_BD,isolation_level=None)
    def __del__(self):
        self.db.close()
        
    def pares(self,palabras):
        palabras=self.limpio(palabras)
        claves=[self.busco_clave(x) for x in palabras.split()]
        claves.sort(reverse=True)
        if len(claves)%2>0:
            claves+=[-1] #agrego un elto especial para formar ult. par
        par=[]
        for i in range(len(claves)/2):
            par.append([claves[i*2],claves[i*2+1]])
        return par
    
    def genconsulta(self,args):
        'genero el sql de la consulta nueva'

        Sum,SubC='',''
        if len(args)>1:
            'ahora veo el armado de subconsultas'
            suma,subc=[],[]
            subr=r'''inner join (select * from claves 
                where clave1=%d and clave2=%d) as consulta%d
                on tabla.id_sujeto=consulta%d.id_sujeto'''
            subr1=subr.replace(" and clave2=%d",'')
            for i,par in enumerate(args[1:]):
                if par[1]>0:
                    #puntos suma los ptos de las claves 1 y 2
                    suma.append('+ consulta%d.puntos' % i)                    
                    sub=subc.append(subr % (par[0],par[1],i,i))
                else:
                    #puntos1 contiene solo los puntos de la 1ra clave
                    suma.append('+ consulta%d.puntos1' % i)                    
                    sub=subc.append(subr1 % (par[0],i,i))
                
            Sum=' '.join(suma)
            SubC='\n'.join(subc)
        sql=['select distinct tabla.id_sujeto,']
        sql+=['  tabla.puntos %s as totalpuntos' % Sum]
        sql+=['from claves as tabla %s' % SubC]
        sql+=['where tabla.clave1=%d' % args[0][0]]
        if args[0][1]>0:
            sql+=['  and tabla.clave2=%d' % args[0][1]]
        sql+=['order by totalpuntos desc']
        return '\n'.join(sql)
    
    def corre(self,palabras):
        args=self.pares(palabras)
        SQL=self.genconsulta(args)
        cur=self.db.cursor()
        cur.execute(SQL)
        for row in cur:
            yield row[0] #devuelve solo el id_sujeto
        
        
    
    #Estas ultimas funciones son solo para uso en debug
    #no van a ser necesarias al usar la clase en el programa
    
    def consulta(self,palabras):
        args=self.pares(palabras)
        SQL=self.genconsulta(args)
        cur=self.db.cursor()
        cur.execute(SQL)
        return cur
      
    def busco_sujeto(self,id_sujeto):
        '''Tomo un sujeto por id, y devuelvo la clave del nombre'''

        SQL=u'SELECT DISTINCT clave1 FROM claves WHERE id_sujeto=? '
        cur=self.db.cursor()
        cur.execute(SQL, (id_sujeto,))
        filas=[row[0] for row in cur]
        filas.sort

    def busco_sujeto2(self,id_sujeto):
        '''Tomo un sujeto x id, y devuelvo el nombre'''

        SQL=u'''SELECT DISTINCT nombre
            FROM claves INNER JOIN nombres ON claves.clave1=nombres.clave
            WHERE id_sujeto=? '''
        cur=self.db.cursor()
        cur.execute(SQL, (id_sujeto,))
        filas=[row[0] for row in cur]
        return ' '.join(filas)
                

if __name__=="__main__":
    B=Buscador()
    #a=B.busco_clave('')
    #print B.busco_nombre(a)

    b='RAMON'
    print B.pares(b)
    B.consulta(b)



