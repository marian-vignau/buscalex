#!/usr/bin/python
# -*- coding: latin-1 -*-

"""
Programa principal
"""

if __name__ == "__main__":
    import Indizar
    print Indizar.actualizar_copia_local(False)
    import Principal
    Busqueda = Principal.Principal(0)
    Busqueda.MainLoop()

