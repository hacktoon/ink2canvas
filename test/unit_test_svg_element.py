import sys
import unittest

sys.path.append('..')
from inkex import Effect
from ink2canvas.svg.Element import Element


class TestSvgElement(unittest.TestCase):
    def setUp(self):
        self.element = Element()
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/unit_test_svg_element.svg")
        self.node = self.effect.document.getroot()
        
    def testAttrWithNs(self):
        self.element.node = self.node
        returnValue = self.element.attr("width", "ns")
        self.assertEqual(returnValue, "12cm")
        
        
    def testAttrWithoutNs(self):
        self.element.node = self.node
        returnValue = self.element.attr("width")
        self.assertEqual(returnValue, "12cm")
   
if __name__ == '__main__':
    unittest.main()
    
