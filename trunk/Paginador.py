#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
El generador es solo una "plantilla", una clase que finalmente
no se usará sino que solo sirve para desarrollo
'''

            
class Paginador(object):
    """Recibe objetos, y arma un cache con ellos
    El objeto generador es el que controla todo, y 
    debe tener varios metodos asignados para funcionar 
    correctamente.    """
    RESULTADOS=-1
    def __init__(self, generador):
        '''el objeto generador es el que controla todo
        este es solo un uti
        '''
        self.cache=[] #lista de elementos leídos
        self.PAGINA=5 #nro de elementos en cada pagina
        self.gene=generador
        self.corre=self.gene.corre() #inicio el generador
        self.pg_actual=-1
        self.cargando=True #si todavía no fué leído el ultimo elemento
        self.marcados={} #diccionario de elementos marcados. 
                        #Un paginador usarse como generador de otro paginador
                        #"genera solo los elementos marcados en su cache
        self.keys=[]

    def rangoPagina(self,n_pagina):
        desde=self.PAGINA*(n_pagina)
        hasta=min(desde+self.PAGINA,len(self.cache))
        return desde,hasta
        
    def ArmoPagina(self,n_pagina):
        '''Aca junto los elementos seleccionados y lo
        paso al generador para su formateo
        '''
        desde,hasta=self.rangoPagina(n_pagina)
        armado=[]
        if desde<hasta:
            ret=self.gene.formateo(self.cache[desde:hasta])
            estado="Página %d" % (self.pg_actual+1)
            if self.RESULTADOS>=0:
                estado+=" de %d paginas" % (self.UltimaPg() +1)
            return ret, estado
        

    def ExisteYCarga(self,n_pagina):
        '''Se fija si una pagina está cargada en cache, 
        si no trata de cargarla. Si no puede, devuelve False
        '''
        desde,hasta=self.rangoPagina(n_pagina)
        if desde>=hasta and self.cargando:
            self.CargoCache()
            desde,hasta=self.rangoPagina(n_pagina)
        #print desde,hasta,n_pagina
        return (desde<hasta)

    def CargoCache(self):
        '''Pido los objetos para ir cargando la cache
        a medida que solicita otra pagina el objeto generador.
        Arma también un diccionario para poder marcar elementos
        '''
        for n in range(self.PAGINA):
            try:
                key,elto=self.corre.next()
                self.marcados[key]=[0,elto]
                self.cache.append([0,elto])
                self.keys.append(key)
            except StopIteration:
                self.RESULTADOS=len(self.cache)
                self.cargando=False
    
    def PgSiguiente(self):
        '''Carga la pagina siguiente, o devuelve ultima pagina
        '''
        
        if self.ExisteYCarga(self.pg_actual+1):
            self.pg_actual+=1
        return self.ArmoPagina(self.pg_actual)
        
    def PgAnterior(self):
        '''Carga la pagina anterior, o devuelve primera pagina
        '''
        
        if not self.EsPrimeraPg():
            self.pg_actual-=1
        return self.ArmoPagina(self.pg_actual)

    def EsPrimeraPg(self):
        return (self.pg_actual<=0)
    
    def EsUltimaPg(self):
        return (not self.cargando and self.pg_actual>=self.UltimaPg())
        

    def UltimaPg(self):
        x=self.RESULTADOS//self.PAGINA
        if self.RESULTADOS%self.PAGINA > 0:
            x+=1
        return x-1 #las paginas se numeran desde 0


    def Marcar(self,key,marca=None):
        if marca==None:
            self.marcados[key][0]=1-self.marcados[key][0]
        else:
            self.marcados[key][0]=marca

    def GeneCache(self):
        for k,x in zip(self.keys,self.cache):
            yield k,x
    
    def Marcado(self,key,marca):
        return (self.marcados[key][0]==marca)

    
if __name__=='__main__':
    'Llama a una nueva consulta'
    import BusqHTML
    consulta='RAMIREZ JOSE'
    print 'consulta:',consulta
    print '1) Devuelvo consulta %s' % consulta
    gen= BusqHTML.DevuelvoConsulta(consulta)
    for r in gen.corre():
        print r
#    g= Paginador(gen)
#    print g.PgSiguiente()

