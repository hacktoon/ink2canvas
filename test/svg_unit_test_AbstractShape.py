import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.AbstractShape import AbstractShape
from ink2canvas.svg.Element import Element

from ink2canvas.canvas import Canvas


class TestSvgAbstractShape(unittest.TestCase):
    
    def returnsGnode(self, root):
        for node in root:
            tag = node.tag.split("}")[1]
            if tag == "path":
                return node
        return None

    def setUp(self):
        self.canvas = Canvas(0,0)
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/imageToTestAbstractShape.svg")
        self.root = self.effect.document.getroot()
        self.node = self.returnsGnode(self.root)
        self.abstractShape = AbstractShape( None,self.node,self.canvas)

    def testGetStyle(self):
        style = self.abstractShape.get_style()
        strStyle = "fill:#ff0000;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
        hashStyle = dict([i.split(":") for i in strStyle.split(";") if len(i)])
        self.assertEqual(hashStyle,style)

        strStyle = "fill:ff0000;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
        hashStyle = dict([i.split(":") for i in strStyle.split(";") if len(i)])
        self.assertNotEqual(hashStyle,style)

    def testSet_style(self):
        style = self.abstractShape.get_style()
        strStyle = "fill:#ff0000;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
        hashStyle = dict([i.split(":") for i in strStyle.split(";") if len(i)])
        self.abstractShape.set_style(hashStyle)
        print self.abstractShape.ctx.lineJoin

        
    def testX(self):
        
        self.abstractShape.node = self.node
        self.abstractShape.command = "arc"
        
        print self.abstractShape.get_style()
        print "olaaa" 

if __name__ == '__main__':
    unittest.main()