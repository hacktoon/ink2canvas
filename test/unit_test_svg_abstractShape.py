import sys
import unittest

sys.path.append('..')
from inkex import Effect
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
        style = self.abstractShape.getStyle()
        strStyle = "fill:#ff0000;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
        hashStyle = dict([i.split(":") for i in strStyle.split(";") if len(i)])
        self.assertEqual(hashStyle,style)

        strStyle = "fill:ff0000;fill-rule:evenodd;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
        hashStyle = dict([i.split(":") for i in strStyle.split(";") if len(i)])
        self.assertNotEqual(hashStyle,style)

    def testSetStyle(self):
        canvas = Canvas(0,0)
        canvas.setStrokeLinejoin("miter")
        canvas.setStroke("#000000")
        canvas.setStrokeLinecap("butt")
        canvas.setStrokeWidth("1px")
        canvas.setFill("#ff0000")
                      
        stringStyle =self.abstractShape.getStyle() 
        self.abstractShape.setStyle(stringStyle)
        
        self.assertEqual(canvas.code, self.abstractShape.canvasContext.code)
        self.assertEqual(self.abstractShape.canvasContext.style,stringStyle) 
        
    def testHasTransform(self):
        self.assertNotEqual(True, self.abstractShape.hasTransform())
        
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"rect")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(True, canvas.abstractShape.hasTransform())

    def testGetTransform(self):
        
        m11 = (float(1),float(0),float(0.3802532),float(0.92488243),0.0,0.0)
        
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"rect")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        vetor = canvas.abstractShape.getTransform()
        
        self.assertEqual(m11, vetor)
        
    def testHasGradient(self):
        
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_GradienteLinear.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(canvas.abstractShape.gradientHelper.hasGradient("fill"), "linear")
        
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_GradienteRadial.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(canvas.abstractShape.gradientHelper.hasGradient("fill"), "radial")
        
        self.assertNotEqual(self.abstractShape.gradientHelper.hasGradient("fill"),"linear")
        
    def testGetGradientHref(self):
        returnValue ="linearGradient3022"
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_GradienteLinear.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(returnValue,canvas.abstractShape.gradientHelper.getGradientHref("fill"))
        
        returnValue ="ovalGradient3022"
        self.assertNotEqual(returnValue,canvas.abstractShape.gradientHelper.getGradientHref("fill"))
    
    def testHasClip(self):
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_Clip.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertTrue(canvas.abstractShape.hasClip())
        self.assertFalse(self.abstractShape.hasClip())
        
    def testGetClipHref(self):
        returnValue = "clipPath3191"
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado_Clip.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"path")
        canvas.abstractShape = AbstractShape( None,canvas.node,self.canvas, None)
        
        self.assertEqual(canvas.abstractShape.getClipId(),returnValue)
        
    def testStart(self):
        canvas2 = Canvas(0,2)
        canvas2.write("\n// #path3033")
        self.abstractShape.initDraw()
        
        self.assertEqual(self.abstractShape.canvasContext.code,canvas2.code)

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
        self.assertEqual(canvas3.abstractShape.canvasContext.code,canvas4.code)
                        
    def testDraw(self):
        canvas = Canvas(0,1)
        canvas.effect = Effect()
        canvas.document = canvas.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado.svg")
        canvas.root = canvas.effect.document.getroot()
        canvas.node = self.returnsGnode(canvas.root,"rect")
        rect = Rect("rect",canvas.node,canvas, None)
        
        rect.draw()
        
        self.assertEqual(rect.canvasContext.code,['\tctx.transform(1.000000, 0.000000, 0.380253, 0.924882, 0.000000, 0.000000);\n', "\tctx.lineJoin = 'miter';\n", "\tctx.strokeStyle = 'rgb(0, 0, 0)';\n", "\tctx.lineCap = 'butt';\n", '\tctx.lineWidth = 1.012632;\n', "\tctx.fillStyle = 'rgb(0, 0, 255)';\n", '\tctx.beginPath();\n', '\tctx.moveTo(-60.184902, 299.915122);\n', '\tctx.lineTo(-60.184902, 677.860048);\n', '\tctx.quadraticCurveTo(-60.184902, 683.719660, -60.184902, 683.719660);\n', '\tctx.lineTo(431.239998, 683.719660);\n', '\tctx.quadraticCurveTo(431.239998, 683.719660, 431.239998, 677.860048);\n', '\tctx.lineTo(431.239998, 299.915122);\n', '\tctx.quadraticCurveTo(431.239998, 294.055510, 431.239998, 294.055510);\n', '\tctx.lineTo(-60.184902, 294.055510);\n', '\tctx.quadraticCurveTo(-60.184902, 294.055510, -60.184902, 299.915122);\n', '\tctx.fill();\n', '\tctx.stroke();\n'])
        
    def testEnd(self):
        self.abstractShape.endDraw()
        self.assertEqual(self.abstractShape.canvasContext.code, [])
        
        canvas1 = Canvas(0,3)
        canvas1.effect = Effect()
        canvas1.document = canvas1.effect.parse("arquivos_test/unit_test_svg_abstractShape_transformado.svg")
        canvas1.root = canvas1.effect.document.getroot()
        canvas1.node = self.returnsGnode(canvas1.root,"rect")
        canvas1.abstractShape = AbstractShape( None,canvas1.node,canvas1, None)
        canvas1.abstractShape.endDraw()
        
        canvas2 = Canvas(0,2)
        canvas2.restore()
        
        self.assertEqual(canvas1.abstractShape.canvasContext.code, canvas2.code)
         
        
if __name__ == '__main__':
    unittest.main()