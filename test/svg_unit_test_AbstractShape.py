import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.AbstractShape import AbstractShape

import Canvas


class TestSvgAbstractShape(unittest.TestCase):
    def setUp(self):
        self.abstractShape = AbstractShape()
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/circulo.svg")
        self.node = self.effect.document.getroot()
            
    def x(self):
        self.abstractShape.node = self.node
        print self.abstractShape.get_style() 

if __name__ == '__main__':
    unittest.main()