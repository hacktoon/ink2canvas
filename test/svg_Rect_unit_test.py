'''
Created on Apr 25, 2012

@author: bublecamp
'''
import unittest
import sys
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.Rect import Rect
from ink2canvas.canvas import Canvas

class TestRect(unittest.TestCase):
    def setUp(self):
        self.effect = Effect()
        self.document = None
        self.effect.parse("arquivos_test/svg_Rect_unit_test_ComRxRy.svg")
        self.node = None
        self.canvas = Canvas(0, 0)
              
    def findNodeInG(self, root, tag):
        for node in root:
            nodeTag = node.tag.split("}")[1]
            if(nodeTag == 'g'):
                root = node
                break
        for node in root:
            nodeTag = node.tag.split("}")[1]
            if(nodeTag == tag):
                return node
        
    def testExitWithoutRxRy(self):
        self.document = self.effect.parse("arquivos_test/svg_Rect_unit_test_SemRxRy.svg")
        root = self.effect.document.getroot()
        self.rect = Rect(None, self.node, self.canvas, None)
        self.rect.node = self.findNodeInG(root, 'rect')
        x, y, w, h, rx, ry = self.rect.get_data()
        self.assertEqual(x, 40.0)
        self.assertEqual(y, 30.0)
        self.assertEqual(w, 100.0)
        self.assertEqual(h, 150.0)
        self.assertEqual(rx, 0)
        self.assertEqual(ry, 0)
        
    def testExitWithRxRy(self):
        self.document = self.effect.parse("arquivos_test/svg_Rect_unit_test_ComRxRy.svg")
        root = self.effect.document.getroot()
        self.rect = Rect(None, self.node, self.canvas, None)
        self.rect.node = self.findNodeInG(root, 'rect')
        x, y, w, h, rx, ry = self.rect.get_data()
        self.assertEqual(x, 40.0)
        self.assertEqual(y, 30.0)
        self.assertEqual(w, 100.0)
        self.assertEqual(h, 150.0)
        self.assertEqual(rx, 5.0)
        self.assertEqual(ry, 10.0)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()