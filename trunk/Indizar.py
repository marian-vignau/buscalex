#!/usr/bin/env python
# -*- coding: latin-1 -*-

'''
Interfaz de manejo del indizador y toda la complejidad
asociada al manejo de archivos.

El esquema pensado es:
'''
import os, shutil, config
SEPA_LOG='-'*20



def Copiar(src,dst,forzado=False):
    copiar=False
    if not os.path.exists(dst):
        copiar=True
    else:
        if forzado:
            os.remove(dst)
            copiar=True
        elif (os.stat(src).st_ctime != os.stat(dst).st_ctime or
            os.stat(src).st_size != os.stat(dst).st_size):
            os.remove(dst)
            copiar=True
    if copiar:
        try:
            shutil.copy2(src,dst)
        except (IOError, os.error), why:
            print "No puede copiarse %s a %s: %s" % (src, dst, str(why))
            copiar=False
    return copiar


def recupero_log():
    'devuelve los valores del log y la configuracion en un formato html muy simple'
    f=open(config.PATH_LOG,'r')  
    armado=[]
    for line in f.read().split('\n'):
        if line==config.SEPA_LOG:
            armado=['<p>']
        else:
            armado.append(line+'<br>')
    f.close()
    #recupera valores de configuracion
    for k,v in config.param.iteritems():
        armado.append('%s: <b>%s</b><br>'%(k,v))
    return '\n'.join(armado) + '</p>'

def actualizar_copia_local(forzado):
    '''Utilizado al iniciar el programa principal, para actualizar 
    la copia local del indice sqlite. 
    '''
    copiar=False
    if config.MASTER_BD == config.PATH_BD:
        mensaje='Tiene en su PC el ultimo indice generado.'
    elif not os.path.exists(config.MASTER_BD):
        mensaje='Necesita regenerar indices. Consulte con el administrador'
    else:
        if Copiar(config.MASTER_BD,config.PATH_BD):
            mensaje='Actualizacion de indices realizada'
        else:
            mensaje='No pudieron actualizarse los indices'
    return mensaje

def Indizar():
    import Indizador, config
    Indizador.DB_Nombres().actualizo_bd()
    print('\n\nActualizando copia local')
    print actualizar_copia_local(True)
    return True

#exceptuados=['Audi','AUTOSALV','IMPESC','LISTADOS','MEMOS','nomesc','NOMGLO',
#    'NOTAS','Oficios','SETS','tablas']

copiar_subdir=['PARTES','SUJETOS']


def copytree(src, dst, progress, symlinks=0):
    #Extraido del manual de python
    names = os.listdir(src)
    if not os.path.exists(dst):
        os.mkdir(dst)
    progress(src)
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                if os.path.basename(srcname) in copiar_subdir:
                    copytree(srcname, dstname, progress, symlinks)
            else:
                Copiar(srcname, dstname)
                progress('')
        except (IOError, os.error), why:
            progress( "No puede copiarse %s a %s: %s" % (srcname, dstname, str(why)))


if __name__ == "__main__":
    def progress(n):
        if n: 
            print '\n%s' % n,
        else:
            print '.',
    print '\nCopiando %s a %s' % (config.LEX_MESA,config.PATH_LEX)
    copytree(config.LEX_MESA, config.PATH_LEX,progress)
    print '\nRegenerando el indice de consulta en %s' % config.BD_TEMP
    Indizar()

        