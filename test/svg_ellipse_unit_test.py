import sys
import unittest
from inkex import Effect
sys.path.append('..')

import inkex
from ink2canvas.canvas import Canvas
from ink2canvas.svg.Ellipse import Ellipse

class TestSvgEllipse(unittest.TestCase):
    def setUp(self):
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/svg_ellipse_unit_test.svg")
        root = self.effect.document.getroot()
        self.node = self.findTag(root, "ellipse")

        self.canvas = Canvas(0, 0)    
        self.ellipse = Ellipse(None, self.node, self.canvas)
        
    def findTag(self, root, no):
        for node in root:
            tag = node.tag.split("}")[1]
            if tag == no:
                return node
        return ""  
 
    def testGet_Data(self):
        x, y, z, w = self.ellipse.get_data()
        self.assertEqual(x, 60)
        self.assertEqual(y, 70)
        self.assertEqual(z, 250)
        self.assertEqual(w, 100)
        
    def testDraw(self):
        self.ellipse.draw(False)
        self.assertEqual(self.ellipse.ctx.code, ["\tctx.fillStyle = 'rgb(255, 0, 0)';\n", '\tctx.beginPath();\n', '\tctx.transform(0.866025, -0.500000, 0.500000, 0.866025, 900.000000, 200.000000);\n', '\tctx.moveTo(60.000000, -30.000000);\n', '\tctx.bezierCurveTo(198.071187, -30.000000, 310.000000, 14.771525, 310.000000, 70.000000);\n', '\tctx.bezierCurveTo(310.000000, 125.228475, 198.071187, 170.000000, 60.000000, 170.000000);\n', '\tctx.bezierCurveTo(-78.071187, 170.000000, -190.000000, 125.228475, -190.000000, 70.000000);\n', '\tctx.bezierCurveTo(-190.000000, 14.771525, -78.071187, -30.000000, 60.000000, -30.000000);\n', '\tctx.fill();\n'])
        
if __name__ == '__main__':
    unittest.main()

