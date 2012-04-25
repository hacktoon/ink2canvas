import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.AbstractShape import AbstractShape
from ink2canvas.svg.Element import Element

from ink2canvas.canvas import Canvas


class TestSvgAbstractShape(unittest.TestCase):
    
    def returnsGnode(self, root, tag):
        for node in root:
            nodeTag = node.tag.split("}")[1]
            if(nodeTag == 'g'):
                root = node
                break
        for node in root:
            nodeTag = node.tag.split("}")[1]
            if(nodeTag == tag):
                return node

    def setUp(self):
        self.canvas = Canvas(0,0)
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/circulo.svg")
        self.root = self.effect.document.getroot()
        self.node = self.returnsGnode(self.root,"path")
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
        canvas = Canvas(0,0)
        canvas.setStrokeLinejoin("miter")
        canvas.setStroke("#000000")
        canvas.setStrokeLinecap("butt")
        canvas.setStrokeWidth("1px")
        canvas.setFill("#ff0000")
                      
        stringStyle =self.abstractShape.get_style() 
        self.abstractShape.set_style(stringStyle)
        
        self.assertEqual(canvas.code, self.abstractShape.ctx.code)
        self.assertEqual(self.abstractShape.ctx.style,stringStyle) 
        
    def testHas_transform(self):
        self.assertNotEqual(True, self.abstractShape.has_transform())
        
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/desenho_transformado.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"rect")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas)
        
        self.assertEqual(True, canvas.abstractShape.has_transform())

    def testGet_transform(self):
            

if __name__ == '__main__':
    unittest.main()