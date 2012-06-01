import sys
import unittest
import filecmp
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
        
    def testIfLinearGradientColorsAreCorrect(self):
        linearGradientDictionary = self.ink2canvas.core.root.linearGradient
        self.assertEqual(linearGradientDictionary["linearGradient2987"].colorStops["1"], "stop-color:#80e900;stop-opacity:1;") 
        self.assertEqual(linearGradientDictionary["linearGradient2987"].colorStops["0.5"], "stop-color:#807400;stop-opacity:1;") 
        self.assertEqual(linearGradientDictionary["linearGradient2987"].colorStops["0"], "stop-color:#800000;stop-opacity:1;")
    
    def testSetLinearGradient(self):
        output_file = open("arquivos_test/linearGradient.html", "w")
        content = self.ink2canvas.core.canvas.output()
        output_file.write(content.encode("utf-8"))
        output_file.close()
        self.assertTrue(filecmp.cmp("arquivos_test/linearGradient.html", "arquivos_test/linearGradientQueDeveriaSair.html"))

    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()