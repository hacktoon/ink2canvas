'''
Created on May 11, 2012

@author: bublecamp
'''
import unittest
import sys
import inkex
from inkex import Effect
from ink2canvas.svg.Element import Element
sys.path.append('..')

from ink2canvas.svg.Rect import Rect
from ink2canvas.canvas import Canvas
from ink2canvas.Ink2CanvasCore import Ink2CanvasCore

class Test(unittest.TestCase):


    def setUp(self):
        
        self.effect = Effect()
        inkex.Effect.__init__(self.effect)
        self.effect.parse("arquivos_test/svg_Rect_unit_test_ComRxRy.svg")
        self.ink2canvas = Ink2CanvasCore(inkex, self.effect)
        self.root = self.effect.document.getroot()
        self.ink2canvas.canvas = Canvas(500, 500)

    def testName(self):
        self.element = Element()
        self.ink2canvas.createTree(self.root, self.element)
        self.printChildren(self.element)
    
    def printChildren(self, element):
        element.runDraw()
        print self.ink2canvas.canvas.output()
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()