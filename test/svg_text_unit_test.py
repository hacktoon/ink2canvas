import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.Text import Text
from ink2canvas.svg.Element import Element

from ink2canvas.canvas import Canvas


class TestTextAbstractShape(unittest.TestCase):
    
    def setUp(self):
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/svg_text_unit_test.svg")
        self.root = self.effect.document.getroot()
        self.canvas = Canvas(0,0)
        self.node = self.findNodeInG(self.root,"text")   
        self.text = Text( None,self.node,self.canvas, None)

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

    def testGetData(self):
        x, y = self.text.get_data()
        self.assertEqual(x, 188.89853)
        self.assertEqual(y, 117.97108)
    
    def testText_helper(self):
        stringRetornada = self.text.text_helper(self.node)
        self.assertEqual(stringRetornada, "TESTE\n  ")
        
        
    def testset_text_style(self):
        self.text.set_text_style(self.text.get_style())
        self.assertEqual(self.text.ctx.code, ['\tctx.font = "normal normal 40px Sans";\n'])
    
    def testDraw(self):
        self.text.draw(False)
        self.assertEqual(self.text.ctx.code, ['\tctx.transform(0.707107, -0.707107, 0.707107, 0.707107, -44.476826, 225.540250);\n', "\tctx.fillStyle = 'rgb(0, 0, 0)';\n", '\tctx.font = "normal normal 40px Sans";\n', '\tctx.fillText("TESTE", 188.898530, 117.971080);\n'])
    
if __name__ == '__main__':
    unittest.main()
