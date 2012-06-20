import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.AbstractShape import AbstractShape
from ink2canvas.svg.Rect import Rect

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
        self.document = self.effect.parse("arquivos_test/unit_test_svg_abstractShape.svg")
        self.root = self.effect.document.getroot()
        self.node = self.returnsGnode(self.root,"path")
        self.abstractShape = AbstractShape( None,self.node,self.canvas, None)

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
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"rect")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(True, canvas.abstractShape.has_transform())

    def testGet_transform(self):
        "matrix(1,0,0.3802532,0.92488243,0,0)"
        m11 = (float(1),float(0),float(0.3802532),float(0.92488243),0.0,0.0)
        
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"rect")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        vetor = canvas.abstractShape.get_transform()
        
        self.assertEqual(m11, vetor)
    def testHas_Gradient(self):
        
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_GradienteLinear.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(canvas.abstractShape.has_gradient("fill"), "linear")
        
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_GradienteRadial.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(canvas.abstractShape.has_gradient("fill"), "radial")
        
        self.assertNotEqual(self.abstractShape.has_gradient("fill"),"linear")
        
    def test_getGradientHref(self):
        retorno ="linearGradient3022"
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_GradienteLinear.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(retorno,canvas.abstractShape.get_gradient_href("fill"))
        
        retorno ="ovalGradient3022"
        self.assertNotEqual(retorno,canvas.abstractShape.get_gradient_href("fill"))
    
    def test_hasClip(self):
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_Clip.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertTrue(canvas.abstractShape.hasClip())
        self.assertFalse(self.abstractShape.hasClip())
        
    def test_getClipHref(self):
        retorno = "clipPath3191"
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_Clip.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(canvas.abstractShape.getClipId(),retorno)
        
    def test_start(self):
        canvas2 = Canvas(0,2)
        canvas2.write("\n// #path3033")
        self.abstractShape.initDraw()
        
        self.assertEqual(self.abstractShape.ctx.code,canvas2.code)

        canvas3 = Canvas(0,3)
        canvas3.effect = Effect()
        canvas3.document = canvas3.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_Clip.svg")
        canvas3.root = canvas3.effect.document.getroot()
        canvas3.node = self.returnsGnode(canvas3.root,"path")
        canvas3.abstractShape = AbstractShape( None,canvas3.node,canvas3, None)
        
        canvas4 = Canvas(0,4)
        canvas4.write("\n// #path2987")
        canvas4.save()
               
        canvas3.abstractShape.initDraw()
        self.assertEqual(canvas3.abstractShape.ctx.code,canvas4.code)
        
        #canvas.save
        
    def test_draw(self):
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"rect")
        rect = Rect("rect",canvas.node,canvas, None)
        
        rect.draw()
        
        self.assertEqual(rect.ctx.code,['\tctx.transform(1.000000, 0.000000, 0.380253, 0.924882, 0.000000, 0.000000);\n', "\tctx.lineJoin = 'miter';\n", "\tctx.strokeStyle = 'rgb(0, 0, 0)';\n", "\tctx.lineCap = 'butt';\n", '\tctx.lineWidth = 1.012632;\n', "\tctx.fillStyle = 'rgb(0, 0, 255)';\n", '\tctx.beginPath();\n', '\tctx.moveTo(-60.184902, 299.915122);\n', '\tctx.lineTo(-60.184902, 677.860048);\n', '\tctx.quadraticCurveTo(-60.184902, 683.719660, -60.184902, 683.719660);\n', '\tctx.lineTo(431.239998, 683.719660);\n', '\tctx.quadraticCurveTo(431.239998, 683.719660, 431.239998, 677.860048);\n', '\tctx.lineTo(431.239998, 299.915122);\n', '\tctx.quadraticCurveTo(431.239998, 294.055510, 431.239998, 294.055510);\n', '\tctx.lineTo(-60.184902, 294.055510);\n', '\tctx.quadraticCurveTo(-60.184902, 294.055510, -60.184902, 299.915122);\n', '\tctx.fill();\n', '\tctx.stroke();\n'])
        
    def test_end(self):
        self.abstractShape.endDraw()
        self.assertEqual(self.abstractShape.ctx.code, [])
        
        canvas1 = Canvas(0,3)
        canvas1.effect = Effect()
        canvas1.document = canvas1.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado.svg")
        canvas1.root = canvas1.effect.document.getroot()
        canvas1.node = self.returnsGnode(canvas1.root,"rect")
        canvas1.abstractShape = AbstractShape( None,canvas1.node,canvas1, None)
        canvas1.abstractShape.endDraw()
        
        canvas2 = Canvas(0,2)
        canvas2.restore()
        
        self.assertEqual(canvas1.abstractShape.ctx.code, canvas2.code)
         
        
if __name__ == '__main__':
    unittest.main()