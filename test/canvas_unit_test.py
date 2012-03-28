import sys
import unittest
sys.path.append('..')

from mockito.mockito import *
from ink2canvas.canvas import Canvas

class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(100.0, 200.0)
        self.canvasWithContext = Canvas(100.0, 200.0, "foo")
        self.canvas.code = []
        self.string_rgb = "FFBBAA"
        self.rgb = [251, 186, 10]
        
    def testBeginPathIfWritesRight(self):
        self.canvas.beginPath()
        self.assertEqual(self.canvas.code, ["\tctx.beginPath();\n"])
        
    def testBeginPathIfWritesRightWithNewCtx(self):
        self.canvasWithContext.beginPath()
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.beginPath();\n"])
        
    def testWriteCorrectInsertion(self):
        text = "ctx.Texto"
        self.canvas.write(text)
        self.assertEqual(self.canvas.code[0], "\t" + text + "\n")
    
    def testWriteCorrectInsertionWithNewCtx(self):
        text = "ctx.Texto"
        self.canvasWithContext.write(text)
        self.assertEqual(self.canvasWithContext.code[0], "\t" + text.replace("ctx", self.canvasWithContext.obj) + "\n")
    
    def testOutput(self):
        from textwrap import dedent
        output = self.canvas.output()
        expected_output = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <title>Inkscape Output</title>
        </head>
        <body>
            <canvas id='canvas' width='%d' height='%d'></canvas>
            <script>
            var %s = document.getElementById("canvas").getContext("2d");
            %s
            </script>
        </body>
        </html>
        """
        expected_output = dedent(expected_output) % (self.canvas.width, self.canvas.height, self.canvas.obj, "".join(self.canvas.code))
        self.assertEqual(output, expected_output)
    
    def testCreateLinearGradient(self):
        href = "str"
        x1, y1, x2, y2 = 0.0 , 2.0 , 3.0, 4.0
        data = (href, x1, y1, x2, y2)
        expectedList = ["\tvar %s = \
                   ctx.createLinearGradient(%f,%f,%f,%f);\n" % data]
        self.canvas.createLinearGradient(href,x1, y1, x2, y2)
        self.assertEqual(self.canvas.code, expectedList)          
    
    def testCreateRadialGradient(self):
        href = "str"
        cx1, cy1, rx, cx2, cy2, ry = 0.0 , 2.0, 3.0, 4.0, 5.0, 6.0
        data = (href, cx1, cy1, rx, cx2, cy2, ry)
        expectedList = ["\tvar %s = ctx.createRadialGradient\
                   (%f,%f,%f,%f,%f,%f);\n" % data]
        self.canvas.createRadialGradient(href, cx1, cy1, rx, cx2, cy2, ry)
        self.assertEqual(self.canvas.code, expectedList)
    
    def testAddColorStop(self):
        href, pos, color = "href" , 2.0, "color"
        data = (href, pos, color)
        expectedList = ["\t%s.addColorStop(%f, %s);\n" % data]
        self.canvas.addColorStop(href, pos, color)
        self.assertEqual(self.canvas.code, expectedList)
           
    def testSetOpacity(self):
        #Float Test
        value = 2.5
        expectedReturn = "\tctx.globalAlpha = %.1f;\n" % float(value)
        self.canvas.setOpacity(value)
        self.assertEqual(self.canvas.code[0], expectedReturn)
        
        #Integer Test
        value = 2
        expectedReturn = "\tctx.globalAlpha = %.1f;\n" % float(value)
        self.canvas.setOpacity(value)
        self.assertEqual(self.canvas.code[1], expectedReturn)
        
    def testSetFillNoOpacity(self):
        value = "url()"
        self.canvas.setFill(value)
        self.assertEqual(self.canvas.code, [])
        
        value = "0 0 255"
        fill = self.canvas.getColor(value, 1)
        self.canvas.setFill(value)
        self.assertEqual(self.canvas.code[0], "\tctx.fillStyle = %s;\n" % fill)
        
        value = "0 0 254"
        fill = self.canvas.getColor(value, 1)
        self.assertNotEqual(self.canvas.code[0], "\tctx.fillStyle = %s;\n" % fill)
        
    def testSetFillWithOpacity(self):
        self.canvas.style["fill-opacity"] = 0.5
        
        value = "url()"
        self.canvas.setFill(value)
        self.assertEqual(self.canvas.code, [])
        
        value = "0 0 255"
        fill = self.canvas.getColor(value, 0.5)
        self.canvas.setFill(value)
        self.assertEqual(self.canvas.code[0], "\tctx.fillStyle = %s;\n" % fill)
        
        value = "0 0 254"
        fill = self.canvas.getColor(value, 0.5)
        self.assertNotEqual(self.canvas.code[0], "\tctx.fillStyle = %s;\n" % fill)
        
    def testSetStroke(self):
        value = "0 0 255"
        self.canvas.setStroke(value)
        self.assertEqual(self.canvas.code[0], "\tctx.strokeStyle = %s;\n" % self.canvas.getColor(value, 1))
        
        value = "0 0 254"
        self.assertNotEqual(self.canvas.code[0], "\tctx.strokeStyle = %s;\n" % self.canvas.getColor(value, 1))
        
        self.canvas.style["stroke-opacity"] = 0.5
        
        value = "0 0 255"
        self.canvas.setStroke(value)
        self.assertEqual(self.canvas.code[1], "\tctx.strokeStyle = %s;\n" % self.canvas.getColor(value, 0.5))
        
        value = "0 0 254"
        self.assertNotEqual(self.canvas.code[0], "\tctx.strokeStyle = %s;\n" % self.canvas.getColor(value, 0.5))

    def testSetFont(self):
        value = "Fonte"
        self.canvas.setFont(value)
        self.assertEqual(self.canvas.code[0],"\tctx.font = \"%s\";\n" % value)
    
    def testTranslate(self):
        cx = cy = 1.0
        self.canvas.write("ctx.translate(%f, %f);" % (cx, cy))
        self.assertEqual(self.canvas.code[0],"\tctx.translate(%f, %f);\n" % (cx, cy))
        
    def testRotate(self):
        angle = 1.0
        self.canvas.write("ctx.rotate(%f);" % angle)
        self.assertEqual(self.canvas.code[0],"\tctx.rotate(%f);\n" % angle)

    def testsScale(self):
        rx, ry = 1.0, 2.0
        self.canvas.write("ctx.scale(%f, %f);" % (rx, ry))
        self.assertEqual(self.canvas.code[0],"\tctx.scale(%f, %f);\n" % (rx, ry))

    def testsTransform(self):
        m11, m12, m21, m22, dx, dy = 1.0, 2.0, 3.0, 4.0, 5.0, 6.0
        self.canvas.write("ctx.transform(%f, %f, %f, %f, %f, %f);" % (m11, m12, m21, m22, dx, dy))
        self.assertEqual(self.canvas.code[0],"\tctx.transform(%f, %f, %f, %f, %f, %f);\n" % (m11, m12, m21, m22, dx, dy))

if __name__ == '__main__':
    unittest.main()
    