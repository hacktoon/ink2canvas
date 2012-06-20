import sys
import unittest
sys.path.append('..')

class Test(unittest.TestCase):
    def setUp(self):
        self.fileComment = "arquivos_test/comment_unit_test.svg"
        self.fileWithoutComment = "arquivos_test/without_comment_unit_test.svg" 
        
    def testShouldIgnoreSVGWithComments(self):
        f = open(self.fileComment)
        
        text = f.read()
        print text
        #self.assertTrue(filecmp.cmp("arquivos_test/linearGradient.html", "arquivos_test/linearGradientQueDeveriaSair.html"))
    
        


if __name__ == "__main__":
    unittest.main()        