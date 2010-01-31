#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import config,ConfigGUI,wx, Indizador

class Progreso(object):
    '''Para mostrar el progreso de la regeneración de índices
    '''
    def __init__(self,parent):
        self.parent=parent
    def __del__(self):
        if hasattr(self,"dlg"):
            self.dlg.Destroy()
    def iniciar(self,I):
        'Crea e inicia el dialogo de progreso'
        self.Indizador=I
        print 'Total de registros:%d' % self.Indizador.total_registros
        self.unidad=int(self.Indizador.total_registros/100)
#        print '\n'.join(str(dir(self.Indizador)).split(','))
        self.dlg = wx.ProgressDialog("Actualizando indices",
                               "Total registros: %d" % self.Indizador.total_registros,
                               maximum = self.Indizador.total_registros,
                               parent=self.parent,
                               style = wx.PD_CAN_ABORT
                                | wx.PD_APP_MODAL
                                | wx.PD_ELAPSED_TIME
                                | wx.PD_ESTIMATED_TIME
                                #| wx.PD_REMAINING_TIME
                                )
        self.keepGoing = True
           
        
    def mostrar(self):
        'Muestra el progreso en el proceso'
        if self.Indizador.registro % 200==0:
            msg=("Procesados %d de %d registros" % 
                (self.Indizador.registro,self.Indizador.total_registros))
            (self.keepGoing, skip) = self.dlg.Update(self.Indizador.registro, msg)
        return self.keepGoing
    

    def terminar(self):
        'Al finalizar, notifica al usuario y cierra la barra de progreso'
        self.cancelado=(not self.keepGoing)
        if self.cancelado:
            msg='Proceso cancelado\n'
        else:
            msg='Actualización completada\n'
        msg=('%sProcesados %d de %d registros' % 
            (msg,self.Indizador.registro+1,self.Indizador.total_registros))
        (self.keepGoing, skip) = self.dlg.Update(self.Indizador.registro, msg)
        self.parent.DoMsg(msg)
        self.dlg.Destroy()
    
    def cancelado(self):
        return self.cancelado

class ProgresoCopia(object):
    '''Muestra el progreso de la copia de archivos para actualizar copia local
    '''
    def __init__(self,parent,titulo,mensaje):
        'Crea e inicia el dialogo de progreso'
        self.parent=parent
        self.mensaje=mensaje
        self.dlg = wx.ProgressDialog(titulo,
                               self.mensaje,
                               #maximum = self.Indizador.total_registros,
                               parent=self.parent,
                               style = wx.PD_APP_MODAL
                                | wx.PD_ELAPSED_TIME
                                )
        self.keepGoing = True
           
        
    def mostrar(self, msg):
        'Muestra el progreso en el proceso'
        if msg:
            self.mensaje=msg
        (self.keepGoing, skip) = self.dlg.Pulse(self.mensaje)
        return self.keepGoing
    

    def terminar(self):
        'Al finalizar, notifica al usuario y cierra la barra de progreso'
        self.parent.DoMsg('Actualización completada\n')
        self.dlg.Destroy()


class MyConfig(ConfigGUI.Config):
    paths={}
    def DoDir(self,msg,ctrl,key):
        dlg = wx.DirDialog(self, "Directorio del Lex principal",
                          ctrl.GetValue(),
                          style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            v=dlg.GetPath()
            if v>'' and v!=ctrl.GetValue():
                self.paths[key]=v
                ctrl.SetValue(v)
        # Only destroy a dialog after you're done with it.
        dlg.Destroy()   
             
    def DoDirLexMesa(self, event): # wxGlade: Config.<event_handler>
        self.DoDir("Directorio del Lex principal",
            self.txtDirLexMesa, 'LEX_MESA')

    def DoDirPathLex(self, event): # wxGlade: Config.<event_handler>
        self.DoDir("Directorio de copia de trabajo del Lex",
            self.txtDirPathLex, 'PATH_LEX')

    def DoGenerarIndice(self, event):
        if self.paths:
            self.DoMsg('Debe primero aplicar los cambios en la configuración')
            return
        P=Progreso(self)
        Indizador.DB_Nombres(P).actualizo_bd()
    

    def DoAplicar(self, event): # wxGlade: Config.<event_handler>
        'Grabo un nuevo archivo de configuración'
        if not self.paths:
            self.DoMsg("No hay paths para actualizar")
            return
        
        ini,bak='%s/config.ini'%config.PRG_DIR,'%s/config.bak'%config.PRG_DIR
        print Indizador.Actualiza(ini,bak)
        sal,comentario=[],0
        f=open(bak,'r')
        
        for line in f.read().split('\n'):
            if "'''" in line:
                comentario=1-comentario
            elif comentario==0:
                for k,v in self.paths.iteritems():
                    com=''
                    if '=' in line and line.startswith(k):
                        if '#' in line:
                            com=' # %s' % line.split("#",1)[1]
                        line='#antes:%s\n%s=%s' % (line,k,v+com)
            sal.append(line)
        f.close()
        g=open(ini,'w')
        g.write('\n'.join(sal))
        g.close()
        reload(config)
        self.paths.clear()
        self.DoMsg('¡Configuración actualizada!')
#        self.DoMsg('Saliendo del sistema para que los cambios tengan efecto')
#        self.Close()

    def DoSalir(self, event): # wxGlade: Config.<event_handler>
        self.Close()

    def DoMsg(self,msg):
        dlg = wx.MessageDialog(self, msg,
                               'Configuración',
                               wx.OK | wx.ICON_INFORMATION
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def DoCopiar(self, event): # wxGlade: Config.<event_handler>
        if self.paths:
            self.DoMsg('Debe primero aplicar los cambios en la configuración')
            return
        import Indizar
        P=ProgresoCopia(self,"Actualizando copia de trabajo de lex-doctor",
            'Copiando %s a %s' % (config.LEX_MESA,config.PATH_LEX)
            )
        Indizar.copytree(config.LEX_MESA, config.PATH_LEX,P.mostrar)
        P.terminar()



if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyConfig(None, wx.ID_ANY, "")
    app.SetTopWindow(frame_1)
    frame_1.txtDirLexMesa.SetValue(config.LEX_MESA)
    frame_1.txtDirPathLex.SetValue(config.PATH_LEX)
    frame_1.Show()
    app.MainLoop()
