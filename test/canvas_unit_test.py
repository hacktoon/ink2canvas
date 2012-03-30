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


        
      
   


if __name__ == '__main__':
    unittest.main()
    