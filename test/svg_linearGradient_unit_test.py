import sys
import unittest
from ink2canvas.main import Ink2Canvas
sys.path.append('..')

class LinearGradientTest(unittest.TestCase):
    
    def setUp(self):
        self.ink2canvas = Ink2Canvas()
        file = "arquivos_test/linearGradient.svg"
        self.ink2canvas.parse(file)
        self.ink2canvas.effect()
        
    def testIfTheLinearGradientNodeIsCreated(self):
        linearGradientDictionary = self.ink2canvas.core.root.linearGradient
        for linearGradientKey, linearGradientValue in linearGradientDictionary.iteritems():
            if linearGradientValue.link == None:
                self.assertNotEqual([], linearGradientValue.colorStops)
            else:
                self.assertNotEqual(None, linearGradientValue.link)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()