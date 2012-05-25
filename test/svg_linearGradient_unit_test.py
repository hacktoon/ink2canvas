import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.LinearGradient import Lineargradient
from ink2canvas.canvas import Canvas


class LinearGradientTest(unittest.TestCase):
    
    def setUp(self):
        self.canvas = Canvas(0,0)
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/linearGradient.svg")
        root = self.effect.document.getroot()
        self.node = None
        for node in root:
            tag = node.tag.split("}")[1]
            if(tag == 'linearGradient'):
                self.node = node
                break   
        self.linearGradient = Lineargradient(None, self.node, self.canvas, None)
        
    def testIfTheLinearGradientNodeIsCreated(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()