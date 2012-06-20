'''
Created on Apr 13, 2012

@author: bublecamp
'''
import unittest
import sys
from inkex import Effect

sys.path.append('..')

from ink2canvas.svg.G import G
from ink2canvas.canvas import Canvas

class TestSvgG(unittest.TestCase):

    def setUp(self):
        self.effect = Effect()
        
        self.document = self.effect.parse("arquivos_test/unit_test_svg_g.svg")
        root = self.effect.document.getroot()   
        self.node = self.findTag(root, "g")
            
        self.canvas = Canvas(0, 0)
        self.g = G(None, self.node, self.canvas, None)

    def findTag(self, root, no):
        for node in root:
            tag = node.tag.split("}")[1]
            if tag == no:
                return node
        return ""   

    def testDraw(self):
        self.g.draw(False);
        self.assertEqual(self.g.ctx.code, ['\tctx.transform(-0.866025, 0.500000, -0.500000, -0.866025, 0.000000, 0.000000);\n'])

if __name__ == "__main__":
    unittest.main()