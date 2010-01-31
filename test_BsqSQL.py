#!/usr/bin/env python
# -*- coding: latin-1 -*-

import unittest
from BusqSQL import *

class TestNombres(unittest.TestCase):
    def setUp(self):
        self.b=Buscador()
        
    def testPares(self):
        palabras='ramirez juan domingo'
        print self.b.pares(palabras)
        
    def testgenconsulta(self):
        palabras='ramirez juan domingo'
        par=self.b.pares(palabras)
        print self.b.genconsulta(par)
        
if __name__ == '__main__':
    unittest.main()