#!/usr/bin/env python
# -*- coding: latin-1 -*-

#este codigo se ejecuta al importar este modulito
#carga en globals(), para permitir el acceso a los parametros
#como propiedades del modulo
f=open('config.ini','r')
comentario=0
param={}

def agrego_global(vble,valor,visible=True):
    if visible:
        param[vble]=valor
    globals()[vble]=valor


def normal(path):
    path= path.strip().replace("/","\\")
    if path.startswith("\\"):
        path=globals()['PRG_DIR']+path
    elif path.startswith("%"):
        pref,suf=path.split("\\",1)
        path=globals()[pref[1:]]+'\\'+suf
    return path

import os
agrego_global('PRG_DIR',os.getcwd().replace("/","\\"))
agrego_global('SEPA_LOG','-'*20,False)



for line in f.read().split('\n'):
    if "'''" in line:
        comentario=1-comentario
    elif comentario==0:
        #quito los comentarios
        if '#' in line:
            line=line.split('#')[0]
        line.strip()
        if '=' in line:
            vble,valor=line.split('=')
            agrego_global(vble,normal(valor))
              
    
if __name__=='__main__':
    print '\n'.join(['%s="%s"' % (k,globals()[k]) for k in param])