import sys
import unittest
sys.path.append('..')

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
        
    def testPutStyleinCacheFirstElement(self):
        self.canvas.putStyleInCache({'foo': "bar"}) 
        self.assertEqual(self.canvas.styleCache, {'foo': "bar"})

    def testPutStyleInCacheAddSecondElement(self):
        self.canvas.putStyleInCache({'foo': "bar"}) 
        self.canvas.putStyleInCache({'fooo': "baar"}) 
        self.assertEqual(self.canvas.styleCache, {'fooo': "baar", 'foo':"bar"})
        
    def testPutStyleInCacheChangingValue(self):
        self.canvas.putStyleInCache({'foo': "bar"}) 
        self.canvas.putStyleInCache({'foo': "baar"}) 
        self.assertEqual(self.canvas.styleCache, {'foo': "baar"})
        
    def testPutStyleInCacheWithNULLValue(self):
        self.canvas.putStyleInCache({'foo': "bar"})
        self.canvas.putStyleInCache({'foo':""}) 
        self.assertEqual(self.canvas.styleCache, {'foo': "bar"})

    def testGetColorWithALowerThenOne(self): 
        retorno = self.canvas.getColor(self.string_rgb, 0)
        self.assertEqual(retorno, "'rgba(%d, %d, %d, %.1f)'" % (251, 186, 10, 0))
                  
    def testGetColorWithAHigherThenOne(self):
        retorno = self.canvas.getColor(self.string_rgb, 2)
        self.assertEqual(retorno, "'rgb(%d, %d, %d)'" % (251, 186, 10))
        
    def testGetColorWithAEqualToOne(self):
        retorno = self.canvas.getColor(self.string_rgb, 1)
        self.assertEqual(retorno, "'rgb(%d, %d, %d)'" % (251, 186, 10))
        
    def testBezierCurveTo(self):
        self.canvas.bezierCurveTo(4, 6, 2.3, -4, 1, 2)
        self.assertEqual(self.canvas.code, ["\tctx.bezierCurveTo(%f, %f, %f, %f, %f, %f);\n" % (4, 6, 2.3, -4, 1, 2)])
        
    def testBezierCurveToWithNewCtx(self):
        self.canvasWithContext.bezierCurveTo(4, 6, 2, 4, 1, 2)
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.bezierCurveTo(%f, %f, %f, %f, %f, %f);\n" % (4, 6, 2, 4, 1, 2)])
        
    def testRectWithRXAndRY(self):
        self.canvas.rect(4, 6, 2, 4, 1, 2)
        self.assertEqual(self.canvas.code, ['\tctx.moveTo(4.000000, 8.000000);\n', '\tctx.lineTo(4.000000, 8.000000);\n', '\tctx.quadraticCurveTo(4.000000, 10.000000, 5.000000, 10.000000);\n', '\tctx.lineTo(5.000000, 10.000000);\n', '\tctx.quadraticCurveTo(6.000000, 10.000000, 6.000000, 8.000000);\n', '\tctx.lineTo(6.000000, 8.000000);\n', '\tctx.quadraticCurveTo(6.000000, 6.000000, 5.000000, 6.000000);\n', '\tctx.lineTo(5.000000, 6.000000);\n', '\tctx.quadraticCurveTo(4.000000, 6.000000, 4.000000, 8.000000);\n'])
        
    def testRectWithRXAndRYCtx(self):
        self.canvasWithContext.rect(4, 6, 2, 4, 1, 2)
        self.assertEqual(self.canvasWithContext.code, ['\tfoo.moveTo(4.000000, 8.000000);\n', '\tfoo.lineTo(4.000000, 8.000000);\n', '\tfoo.quadraticCurveTo(4.000000, 10.000000, 5.000000, 10.000000);\n', '\tfoo.lineTo(5.000000, 10.000000);\n', '\tfoo.quadraticCurveTo(6.000000, 10.000000, 6.000000, 8.000000);\n', '\tfoo.lineTo(6.000000, 8.000000);\n', '\tfoo.quadraticCurveTo(6.000000, 6.000000, 5.000000, 6.000000);\n', '\tfoo.lineTo(5.000000, 6.000000);\n', '\tfoo.quadraticCurveTo(4.000000, 6.000000, 4.000000, 8.000000);\n'])
    
    def testRectWithoutRXAndRY(self):
        self.canvas.rect(4, 6, 2, 4)
        self.assertEqual(self.canvas.code, ["\tctx.rect(%f, %f, %f, %f);\n" % (4, 6, 2, 4)])
        
    def testRectWithoutRXAndRYCtx(self):
        self.canvasWithContext.rect(4, 6, 2, 4)
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.rect(%f, %f, %f, %f);\n" % (4, 6, 2, 4)])
                
    def testRectWithRX(self):
        self.canvas.rect(4, 6, 2, 4, 1)
        self.assertEqual(self.canvas.code, ['\tctx.moveTo(4.000000, 6.000000);\n', '\tctx.lineTo(4.000000, 10.000000);\n', '\tctx.quadraticCurveTo(4.000000, 10.000000, 5.000000, 10.000000);\n', '\tctx.lineTo(5.000000, 10.000000);\n', '\tctx.quadraticCurveTo(6.000000, 10.000000, 6.000000, 10.000000);\n', '\tctx.lineTo(6.000000, 6.000000);\n', '\tctx.quadraticCurveTo(6.000000, 6.000000, 5.000000, 6.000000);\n', '\tctx.lineTo(5.000000, 6.000000);\n', '\tctx.quadraticCurveTo(4.000000, 6.000000, 4.000000, 6.000000);\n'])
        
    def testRectWithRXCtx(self):
        self.canvasWithContext.rect(4, 6, 2, 4, 1)
        self.assertEqual(self.canvasWithContext.code, ['\tfoo.moveTo(4.000000, 6.000000);\n', '\tfoo.lineTo(4.000000, 10.000000);\n', '\tfoo.quadraticCurveTo(4.000000, 10.000000, 5.000000, 10.000000);\n', '\tfoo.lineTo(5.000000, 10.000000);\n', '\tfoo.quadraticCurveTo(6.000000, 10.000000, 6.000000, 10.000000);\n', '\tfoo.lineTo(6.000000, 6.000000);\n', '\tfoo.quadraticCurveTo(6.000000, 6.000000, 5.000000, 6.000000);\n', '\tfoo.lineTo(5.000000, 6.000000);\n', '\tfoo.quadraticCurveTo(4.000000, 6.000000, 4.000000, 6.000000);\n'])
        
    def testLineTo(self):
        self.canvas.lineTo(4, 6)
        self.assertEqual(self.canvas.code, ["\tctx.lineTo(%f, %f);\n" % (4, 6)])
        
    def testLineToWithNewCtx(self):
        self.canvasWithContext.lineTo(4, 6)
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.lineTo(%f, %f);\n" % (4, 6)])
 
    def testMoveTo(self):
        self.canvas.moveTo(4, 6)
        self.assertEqual(self.canvas.code, ["\tctx.moveTo(%f, %f);\n" % (4, 6)])
        
    def testMoveToWithNewCtx(self):
        self.canvasWithContext.moveTo(4, 6)
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.moveTo(%f, %f);\n" % (4, 6)])
 
    def testSetStrokeMiterlimit(self):
        self.canvas.setStrokeMiterlimit("banana")
        self.assertEqual(self.canvas.code, ["\tctx.miterLimit = %s;\n" % "banana"])
        
    def testSetStrokeMiterlimitNewCtx(self):
        self.canvasWithContext.setStrokeMiterlimit("banana")
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.miterLimit = %s;\n" % "banana"])
        
    def testSetStrokeLinejoin(self):
        self.canvas.setStrokeLinejoin("banana")
        self.assertEqual(self.canvas.code, ["\tctx.lineJoin = '%s';\n" % "banana"])
        
    def testSetStrokeLinejoinNewCtx(self):
        self.canvasWithContext.setStrokeLinejoin("banana")
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.lineJoin = '%s';\n" % "banana"])
        
    def testSetStrokeLinecap(self):
        self.canvas.setStrokeLinecap("banana")
        self.assertEqual(self.canvas.code, ["\tctx.lineCap = '%s';\n" % "banana"])
        
    def testSetStrokeLinecapNewCtx(self):
        self.canvasWithContext.setStrokeLinecap("banana")
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.lineCap = '%s';\n" % "banana"])
    
    def testSetStrokeWidth(self):
        self.canvas.setStrokeWidth("2px")
        self.assertEqual(self.canvas.code, ["\tctx.lineWidth = %f;\n" % 2])
        
    def testSetStrokeWidthNewCtx(self):
        self.canvasWithContext.setStrokeWidth("2px")
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.lineWidth = %f;\n" % 2])

    def testQuadraticCurveTo(self):
        self.canvas.quadraticCurveTo(4, 6, 2.3, -4)
        self.assertEqual(self.canvas.code, ["\tctx.quadraticCurveTo(%f, %f, %f, %f);\n" % (4, 6, 2.3, -4)])
        
    def testQuadraticCurveToWithNewCtx(self):
        self.canvasWithContext.quadraticCurveTo(4, 6, 2, 4)
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.quadraticCurveTo(%f, %f, %f, %f);\n" % (4, 6, 2, 4)])
       
    def testFillText(self):
        self.canvas.fillText("batata", 4, 6)
        self.assertEqual(self.canvas.code, ["\tctx.fillText(\"%s\", %f, %f);\n" % ("batata", 4, 6)])
        
    def testFillTextWithNewCtx(self):
        self.canvasWithContext.fillText("batata", 4, 6)
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.fillText(\"%s\", %f, %f);\n" % ("batata", 4, 6)])
   
    def testSave(self):
        self.canvas.save()
        self.assertEqual(self.canvas.code, ["\tctx.save();\n"])
        
    def testSaveWithNewCtx(self):
        self.canvasWithContext.save()
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.save();\n"])
     
    def testClip(self):
        self.canvas.clip()
        self.assertEqual(self.canvas.code, ["\tctx.clip();\n"])
        
    def testClipWithNewCtx(self):
        self.canvasWithContext.clip()
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.clip();\n"]) 
    
    def testArc(self):
        self.canvas.arc(1, 2, 3, 4, 5, 1)
        self.assertEqual(self.canvas.code, ["\tctx.arc(%f, %f, %f, %f, %.8f, %d);\n" % (1, 2, 3, 4, 5, 1)])
        
    def testArcWithNewCtx(self):
        self.canvasWithContext.arc(1, 2, 3, 4, 5, 1)
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.arc(%f, %f, %f, %f, %.8f, %d);\n" % (1, 2, 3, 4, 5, 1)])
    
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
        self.canvas.translate(cx, cy)
        self.assertEqual(self.canvas.code[0],"\tctx.translate(%f, %f);\n" % (cx, cy))
        
    def testRotate(self):
        angle = 1.0
        self.canvas.rotate(angle)
        self.assertEqual(self.canvas.code[0],"\tctx.rotate(%f);\n" % angle)

    def testsScale(self):
        rx, ry = 1.0, 2.0
        self.canvas.scale(rx, ry)
        self.assertEqual(self.canvas.code[0],"\tctx.scale(%f, %f);\n" % (rx, ry))

    def testsTransform(self):
        m11, m12, m21, m22, dx, dy = 1.0, 2.0, 3.0, 4.0, 5.0, 6.0
        self.canvas.transform(m11, m12, m21, m22, dx, dy)
        self.assertEqual(self.canvas.code[0],"\tctx.transform(%f, %f, %f, %f, %f, %f);\n" % (m11, m12, m21, m22, dx, dy))
                                    
    def testRestore(self):
        self.canvas.restore()
        self.assertEqual(self.canvas.code[0],"\tctx.restore();\n")
        
    def testSetGradient(self):
        retorno = self.canvas.setGradient(None)
        self.assertEqual(retorno,None)
        
    def testClosePath(self):
        text1, text2, text3 = "ctx.closePath();","ctx.fill();","ctx.stroke();"
        self.canvas.closePath(False)
        self.assertEquals(self.canvas.code, [])
        
        self.canvas.style["fill"] = "none"
        self.canvas.style["stroke"] = "none"
        self.canvas.closePath(True)                                    
        self.assertEqual(self.canvas.code[0],"\t"+text1+"\n")

        self.canvas.style["fill"] = "fill"
        self.canvas.style["stroke"] = "stroke"
        self.canvas.closePath(True)
        self.assertEqual(self.canvas.code[1],"\t"+text1+"\n")
        self.assertEqual(self.canvas.code[2],"\t"+text2+"\n")
        self.assertEqual(self.canvas.code[3],"\t"+text3+"\n")

        
if __name__ == '__main__':
    unittest.main()

