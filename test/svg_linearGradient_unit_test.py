import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.LinearGradient import LinearGradient

class LinearGradientTest(unittest.TestCase):


    def setUp(self):
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/linearGradient.svg")
        root = self.effect.document.getroot()
        
        for node in root:
            tag = node.tag.split("}")[1]
            if(tag == 'linearGradient'):
                self.node = node
                break   
        self.linearGradient = LinearGradient(None, self.node, self.canvas, None)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()