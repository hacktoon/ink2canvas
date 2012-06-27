import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.Text import Text

from ink2canvas.canvas import Canvas

class TestText(unittest.TestCase):
    
    def setUp(self):
        self.effect = Effect()
        self.document = self.effect.parse("TestFiles/unit_test_svg_text.svg")
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
        x, y = self.text.getData()
        self.assertEqual(x, 188.89853)
        self.assertEqual(y, 117.97108)
    
    def testTextHelper(self):
        stringRetornada = self.text.textHelper(self.node)
        self.assertEqual(stringRetornada, "TESTE\n  ")
        
        
    def testSetTextStyle(self):
        self.text.setTextStyle(self.text.getStyle())
        self.assertEqual(self.text.canvasContext.code, ['\tctx.font = "normal normal 40px Sans";\n'])
    
    def testDraw(self):
        self.text.draw(False)
        self.assertEqual(self.text.canvasContext.code, ['\tctx.transform(0.707107, -0.707107, 0.707107, 0.707107, -44.476826, 225.540250);\n', "\tctx.fillStyle = 'rgb(0, 0, 0)';\n", '\tctx.font = "normal normal 40px Sans";\n', '\tctx.fillText("TESTE", 188.898530, 117.971080);\n'])
    
if __name__ == '__main__':
    unittest.main()
