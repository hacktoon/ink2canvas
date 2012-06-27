import sys
import unittest

sys.path.append('..') 
from inkex import Effect
from ink2canvas.svg.Circle import Circle


class TestSvgCircle(unittest.TestCase):
    def setUp(self):
        self.circle = Circle(12, 12, 12, None)
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/unit_test_svg_circle.svg")
        root = self.effect.document.getroot()
        
        for node in root:
            tag = node.tag.split("}")[1]
            if(tag == 'circle'):
                self.node = node
                break
 
    def testGetDataCx(self):
        self.circle.node = self.node
        data = self.circle.getData()
        self.assertEqual(data[0], 600)
        
    def testGetDataCy(self):
        self.circle.node = self.node
        data = self.circle.getData()
        self.assertEqual(data[1], 200)
        
    def testGetDataR(self):
        self.circle.node = self.node
        data = self.circle.getData()
        self.assertEqual(data[2], 100)

if __name__ == '__main__':
    unittest.main()

