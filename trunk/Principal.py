#!/usr/bin/python
# -*- coding: latin-1 -*-

"""
Programa que ejecuta la interfaz gráfica
"""


from BusqGUI import MyFrame
import wx
import BusqHTML, config, Indizar
from Paginador import Paginador
ACERCA_DE='''<img src="%s/icons/BusSujetos2_G.png"></img><br>
            <h1>Busca Lex 1.0</h1>
            <p>Desarrollado por María Andrea Vignau mavignau@gmail.com<br>
            para el Pder Judicial de la Provincia del Chaco
            </p>''' % config.PRG_DIR

def SetHourGlass(object):
    object.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))

def SetCursorArrow(object):
    object.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

class fraSearch(MyFrame):
    def __init__(self, *args, **kwds):
        MyFrame.__init__(self,*args, **kwds)
        self.Print=wx.html.HtmlEasyPrinting(name="Printing", parentWindow=None)
        self.HTML=''
        self.SetPage(ACERCA_DE)

    def DoAcerca(self, event): # wxGlade: MyFrame.<event_handler>
        self.SetPage(ACERCA_DE)

    def DoVerConfig(self, event): # wxGlade: MyFrame.<event_handler>
        self.SetPage(Indizar.recupero_log())

    def DoCorrer(self, event): # wxGlade: MyFrame.<event_handler>
        'Llama a una nueva consulta'
        consulta=self.txtBusqueda.GetValue().strip()
        if consulta>'':
            SetHourGlass(self)
            gen= BusqHTML.DevuelvoConsulta(consulta)
            self.Paginador= Paginador(gen)
            self.DoSiguiente(event)
            SetCursorArrow(self)
        else:
            self.SetPage('<p>Debe ingresar nombres para buscar</p>')
    
    def DoReiniciar(self, event): # wxGlade: MyFrame.<event_handler>
        self.DoCorrer(event)

    def DoSiguiente(self, event): # wxGlade: MyFrame.<event_handler>
        'Pide una pagina de resultados'
        if hasattr(self,"Paginador"):
            SetHourGlass(self)
            HTML,estado=self.Paginador.PgSiguiente()
            self.SetPage(HTML,estado)
            
            SetCursorArrow(self)
    
    def DoAnterior(self, event):
        'Pide una pagina de resultados'
        if hasattr(self,"Paginador"):
            SetHourGlass(self)
            HTML,estado=self.Paginador.PgAnterior()
            self.SetPage(HTML,estado)
            SetCursorArrow(self)

    def SetPage(self,HTML_I,estado=""):
        HTML='<html><body>'
        HTML+=HTML_I+'</body></html>'
        self.HTML=HTML
        self.SetStatusText(estado,0)
        self.htmlResult.SetPage(HTML)
        if hasattr(self,"Paginador"):
            self.fraBusqueda_toolbar.EnableTool(2,(not self.Paginador.EsPrimeraPg()))
            self.fraBusqueda_toolbar.EnableTool(3,(not self.Paginador.EsUltimaPg()))

       
    def DoImprimir(self, event): # wxGlade: MyFrame.<event_handler>
        self.Print.PrintText(self.HTML)

    def DoCopiar(self, event): # wxGlade: MyFrame.<event_handler>
        if wx.TheClipboard.Open():
            texto=self.htmlResult.ToText()
            text_data = wx.TextDataObject(texto)
            wx.TheClipboard.SetData(text_data)
            wx.TheClipboard.Close()


class Principal(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        fraBusqueda = fraSearch(None, -1, "")
        self.SetTopWindow(fraBusqueda)
        fraBusqueda.Show()
        return 1

# end of class MyApp

if __name__ == "__main__":
    Busqueda = Principal(0)
    Busqueda.MainLoop()
