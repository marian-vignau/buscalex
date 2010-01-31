#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Aca esta la generacion de la base de datos en si misma

Proceso:
. leer del dbf los campos correspondientes.
. Filtrar caracteres raros, sacar simbolos irrelevantes
. procesar y generar un diccionario con cada simbolo y su puntaje posicional
. Convertir cada simbolo en su numero
. Generar los pares de simbolos, sumar su puntaje, y grabar el del 1ro
. Grabar
Nota:
Puntaje posicional: Según el lugar que ocupa una palabra dentro de un
nombre, es + o - importante para identificar a una persona, Por ej:
Si busco "GUILLERMO", debe responder 1ro los q tienen apellido GUILLERMO,
2do los q tienen 1er nombre GUILLERMO, y 3ro los que lo tienen como 2do nombre.
Por éso se asignan distintos puntajes posicionales a cada simbolo (o palabra)
que compone el nombre.
Para hacer: también sería importante responder tomando en cuenta el orden en
q ingresó la consulta el operador.
'''

import sqlite3,time, config, datetime, sys, os, shutil
import dbfpy.dbf


MAX_ID=0

fecha=datetime.datetime.now #con esto creo una abreviatura

def debug(tupla):
    #print(tupla)
    pass

class Nombres(object):
    '''Contiene funciones relacionadas a la tabla de nombres
    (o palabras o símbolos)
    '''
    def busco_clave(self,clave):
        '''Tomo un nombre, y me fijo si ya está en la BD
        si esta, leo el numero asignado al mismo'''
        SQL=u'SELECT clave FROM nombres WHERE nombre=? '
        cur=self.db.cursor()
        cur.execute(SQL, (clave,))
        filas=[row[0] for row in cur]
        if filas:
            return min(filas)
        else:
            return 0

    def limpio(self,nombre):
        '''devuelve el nombre sin partes raras'''
        nom=nombre.upper().replace('"','').replace("'",'').replace('(A)','')
        nom=nom.replace(' DEL ',' ')
        if not type(nom) is unicode:
            return unicode(nom,errors='ignore')
        else:
            return nom

    def agrego_clave(self,clave):
        '''Aca tomo un nombre, y me fijo si ya está en la BD
        si esta, leo el numero asignado al mismo
        si no, genero una nueva clave'''
        id = self.busco_clave(clave)
        if id: return id
        else:
            #si no lo encuentra, lo inserta
            SQL='''INSERT INTO nombres ("nombre") VALUES ("%s")'''
            self.db.cursor().execute(SQL%clave)
            id = self.busco_clave(clave)
            if id:
                return id
            else:
                raise 'ERROR EN ID'

class Progreso(object):
    def iniciar(self,I):
        self.Indizador=I
        print 'Total de registros:%d' % self.Indizador.total_registros
        self.unidad=int(self.Indizador.total_registros/100)
        self.cancelado=False
#        print '\n'.join(str(dir(self.Indizador)).split(','))

    def mostrar(self):
        #Muestro los puntitos
        if self.Indizador.registro>0 and self.Indizador.registro % self.unidad==0:
            print '.',
            if self.Indizador.registro % (self.unidad*10)==0:
                print self.Indizador.registro
#        if self.Indizador.registro>50:
#            self.cancelado=True
        return not self.cancelado

    def terminar(self):
        if self.cancelado:
            print ('\nProceso interrumpido')
        print ('\nProcesados con %d de %d registros' % 
        (self.Indizador.registro,self.Indizador.total_registros))
        
    def cancelado(self):
        return self.cancelado
    
class Indizador(Nombres):
    '''Clase generadora de la Base de Datos de indice
    '''
    puntaje={'APEL': 21, 'NOMB': 12, 'NOM2': 6}
    
    def __init__(self,p=Progreso()):
        self.dbf1 = dbfpy.dbf.Dbf()
        self.dbf1.openFile('%s/SUJETOS.dbf' % config.PATH_LEX, readOnly=1)
        self.dbf1.reportOn()
        self.total_registros=len(self.dbf1)
        self.registro=0
        self.presentador=p
        self.presentador.iniciar(self)

    def evaluar(self, palabras, punto):
        '''aca reparto los puntos disponibles
        siempre la primera palabra tiene doble puntaje identificatorio
        '''
        parte=punto/(len(palabras)+1)
        puntos=[parte for n in palabras]
        puntos[0]+=parte #el 1er nombre o apellido vale doble
        return puntos

    def grabar(self,id_sujeto,claves,puntos,puntos1):
        '''grabo la clave'''
        SQL='''INSERT INTO claves ("clave1", "clave2", "puntos", "puntos1", 
            "id_sujeto") VALUES (?,?,?,?,?)'''
        cur=self.db.cursor()
        cur.execute(SQL, (claves[0],claves[1],puntos,puntos1,id_sujeto))
        #~ cur.commit()


    def pares(self,lst):
        '''devuelve todos los pares ordenados 
        posibles de elementos de una lista'''
        if len(lst)<=1:
            return None
        else:
            lista=[]
            for y in lst[1:]:
                lista.append([lst[0],y])
            ret=self.pares(lst[1:])
            if ret:
                for n in ret:
                    lista.append(n)
            return lista

    def grabo_pares(self,id_sujeto,dicc_ptos):
        '''Aca formo los pares de claves para cada sujeto
        y los grabo en la base de datos'''
        simbolos=dicc_ptos.keys()
        simbolos.sort(reverse=True)
        dicc_ptos[0]=0
        if len(simbolos)==1:
            'caso especial: cuando solo aparece un alias, por ejemplo'
            lista=[simbolos+[0]]
        else:
            lista=self.pares(simbolos)
            '''agrego la ultima palabra acompañada de cero,
            sino en algunos casos no podría ser encontrada'''
            lista.append([simbolos[-1],0])
        debug(dicc_ptos)
        
        for par in lista:
            debug(par)
            ptos=dicc_ptos[par[0]]+dicc_ptos[par[1]]
            debug((id_sujeto,par,ptos))
            self.grabar(id_sujeto,par,ptos,dicc_ptos[par[0]])

    def leo_lex(self):
        'leo los datos crudos de la tabla original'
        for self.registro in range(self.total_registros):
            yield(self.dbf1[self.registro])

    def generar(self,):
        '''leo la informacion directamente por el dbf
        antes:leo la informacion a traves de la api del lex'
        print 'lex: %s' % config.PATH_LEX
        tabla=Partes.Sujetos(config.PATH_LEX)'''
        
        for rec in self.leo_lex():
            id=rec['SUJE']
            dicc_ptos={}
            for campo in self.puntaje.keys():
                valor=self.limpio(rec[campo])
                if valor:
                    debug((campo,valor))
                    palabras=valor.split()
                    puntos=self.evaluar(palabras,self.puntaje[campo])
                    claves=[self.agrego_clave(p) for p in palabras]
                    d=dict(zip(claves,puntos))
                    dicc_ptos.update(d)
            self.grabo_pares(id,dicc_ptos)
            if not self.presentador.mostrar():
                break
        self.dbf1.close()
        self.presentador.terminar()


class DB_Nombres(Indizador):
    '''En esta clase se maneja la creacion, generacion de las tablas
    e indizado de las mismas
    '''
        
    def creo_db(self,path):
        '''creacion inicial de la bd'''
        self.db=sqlite3.connect(path,isolation_level=None)
        self.db.cursor().execute('PRAGMA synchronous = OFF;') #desactivo control trasaccional
        self.DoSQL('DROP INDEX "I_CLAVE"')
        self.DoSQL('DROP INDEX "I_SUJETO"')
        self.DoSQL('DROP INDEX "I_PUNTOS"')        
        self.DoSQL('DROP TABLE "claves"')
        
        SQL='''CREATE TABLE "claves"
            ("clave1" INTEGER, "clave2" INTEGER, "puntos" INTEGER, 
            "puntos1" INTEGER, "id_sujeto" INTEGER)'''
        self.DoSQL(SQL)
        SQL='''CREATE TABLE "nombres"
            ("clave" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
            "nombre" char NOT NULL )'''
        self.DoSQL(SQL)
        SQL='''CREATE INDEX "I_NOMBRE" ON "nombres" ("nombre" ASC)'''
        self.DoSQL(SQL)
        return self.db

    def DoSQL(self,SQL):
        try:
            self.db.cursor().execute(SQL)
        except sqlite3.OperationalError:
            print "sqlite3.OperationalError"
            print sys.exc_info()
            print SQL
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def creo_indices(self):
        SQL='''CREATE INDEX "I_CLAVE" ON "claves" ("clave1" ASC, "clave2" ASC)'''
        self.DoSQL(SQL)
        SQL='''CREATE INDEX "I_SUJETO" ON "claves" ("id_sujeto" ASC)'''
        self.DoSQL(SQL)
        SQL='''CREATE INDEX "I_PUNTOS" ON "claves" ("puntos" ASC)'''
        self.DoSQL(SQL)

    def actualizo_bd(self):
        'La indizacion en si misma'
        ini=time.time()
        inicio=fecha().strftime("%d/%m/%Y %H:%M:%S")
        self.creo_db(config.BD_TEMP)
        self.generar()
        self.creo_indices()
        self.db.close()
        fin=fecha().strftime("%d/%m/%Y %H:%M:%S")
        if self.presentador.cancelado:
            res='Proceso interrumpido'
        else:
            
            res=Actualiza(config.BD_TEMP,config.MASTER_BD)
            print '----',res
        #Grabo el log
        f=open(config.PATH_LOG,'a')
        f.write(config.SEPA_LOG)
        f.write('\nInicio del proceso: <b>%s</b>\n' % inicio)
        f.write('Fin del proceso: <b>%s</b>\n' % fin)
        f.write('Registros procesados: <b>%d</b>\n' % self.registro)
        f.write('Archivo generado: <b>"%s"</b>\n' % config.BD_TEMP)
        f.write('%s\n' % res)
        f.close()

def Actualiza(origen, destino, ver_fecha=True):
    print "act %s en %s" % (origen,destino)

    if origen==destino:
        return "Origen y destino son iguales"
    else:
        if not os.path.exists(origen):
            return "No existe el archivo de origen"
        elif os.path.exists(destino):
            if ver_fecha:
                if os.stat(origen).st_ctime==os.stat(destino).st_ctime:
                    return "Ambos archivos son de la misma fecha"
            
            os.remove(destino)
        shutil.copy(origen, destino)
        return "Copiado %s en %s" % (origen,destino)


if __name__=='__main__':
    I=DB_Nombres()
    print config.BD_TEMP
    I.actualizo_bd()
    #~ print recupero_log()