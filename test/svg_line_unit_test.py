import sys
import unittest
from inkex import Effect
sys.path.append('..')

import inkex
from ink2canvas.canvas import Canvas
from ink2canvas.svg.Line import Line

class TestSvgLine(unittest.TestCase):
    def setUp(self):
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/line2.svg")
        root = self.effect.document.getroot()
        #self.node = self.findTag(root, "g")
        self.node = self.findTag(root, "line")

        self.canvas = Canvas(0, 0)    
        self.line = Line(None, self.node, self.canvas)
        
    def findTag(self, root, no):
        for node in root:
            tag = node.tag.split("}")[1]
            if tag == no:
                return node
        return ""  
 
    def testGet_Data(self):
        x, y = self.line.get_data()
        self.assertEqual(x, ('M', (100.0, 300.0)) )
        self.assertEqual(y, ('L', (300.0, 100.0)) )
        
if __name__ == '__main__':
    unittest.main()

