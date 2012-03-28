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
        
            
if __name__ == '__main__':
    unittest.main()
    