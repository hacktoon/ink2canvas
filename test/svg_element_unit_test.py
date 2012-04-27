import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.Element import Element


class TestSvgElement(unittest.TestCase):
    def setUp(self):
        self.element = Element()
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/CirculoVerdadeiro.svg")
        self.node = self.effect.document.getroot()
        
    def testAttrWithNs(self):
        self.element.node = self.node
        retorno = self.element.attr("width", "ns")
        self.assertEqual(retorno, "12cm")
        
        
    def testAttrWithoutNs(self):
        self.element.node = self.node
        retorno = self.element.attr("width")
        self.assertEqual(retorno, "12cm")
   
if __name__ == '__main__':
    unittest.main()
    
