import sys
import unittest
sys.path.append('..')

from mockito.mockito import *
from ink2canvas.canvas import Canvas

class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(100.0, 200.0)
        #testar CanvasWithContext qdo tiver write na funcao
        self.canvasWithContext = Canvas(100.0, 200.0, "foo")
        self.canvas.code = []
        self.string_rgb = "FFBBAA"
        self.rgb = [251, 186, 10]
        
    #BeginPath()    
    def testBeginPathIfWritesRight(self):
        self.canvas.beginPath()
        self.assertEqual(self.canvas.code, ["\tctx.beginPath();\n"])
        
    def testBeginPathIfWritesRightWithNewCtx(self):
        self.canvasWithContext.beginPath()
        self.assertEqual(self.canvasWithContext.code, ["\tfoo.beginPath();\n"])
        
    #EqualStyle
    def testEqualStyleIfKeyIsInStyleCache(self):
        self.canvas.styleCache = {'ola':1}
        self.assertEqual(self.canvas.equalStyle(0,'ola'), True)

        
      
   


if __name__ == '__main__':
    unittest.main()
    