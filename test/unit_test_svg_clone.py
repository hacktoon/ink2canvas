import unittest

from ink2canvas.main import Ink2Canvas
from ink2canvas.svg import Use, G


class TestSvgClone(unittest.TestCase):
    
    def setUp(self):
        self.ink2canvas = Ink2Canvas()
        svgInput = "TestFiles/unit_test_clone_quadrados.svg"
        self.ink2canvas.parse(svgInput)
        self.ink2canvas.effect()
        self.root = self.ink2canvas.core.root 
        self.ListofUses = []
                
    def createUseList(self, nodesThatShouldBeDrawn):
       
        for presentNode in nodesThatShouldBeDrawn:
            if(isinstance(presentNode, Use)):
                self.ListofUses.append(presentNode)
            if(isinstance(presentNode, G)):
                self.createUseList(presentNode.children)
                    
    def searchForUSETag(self, nodesThatShouldBeDrawn):
        returnValue = False
        for presentNode in nodesThatShouldBeDrawn:
            if(isinstance(presentNode, Use)):
                return True
            if(isinstance(presentNode, G)):
                returnValue = self.searchForUSETag(presentNode.children)
                if(returnValue):
                    break
        return returnValue
        
    def testCloneCreate(self):
        rootTree = self.root
        boolean = self.searchForUSETag(rootTree.getDrawable())
        self.assertEqual(boolean, True) 
    
    def testSearchCloneId(self):
        self.createUseList(self.root.getDrawable())
        for eachUSETag in self.ListofUses:
            targetId = eachUSETag.getCloneId()
            self.assertIsNotNone(targetId)
            IdElement = self.ink2canvas.core.root.searchElementById(targetId, self.root.getDrawable())
            self.assertIsNotNone(IdElement)
    
    def testCLoneBuffer(self):
        svg_input = "TestFiles/unit_test_clone_identico.svg"
        self.ink2canvas.parse(svg_input)
        self.ink2canvas.effect()
        self.root = self.ink2canvas.core.root 
        self.ListofUses = []
        pass
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCLoneCreate']
    unittest.main()
