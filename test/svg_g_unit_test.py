'''
Created on Apr 13, 2012

@author: bublecamp
'''
import unittest
import sys
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.G import G
from ink2canvas.svg.AbstractShape import AbstractShape
from ink2canvas.svg.Element import Element

class TestSvgG(unittest.TestCase):

    def setUp(self):
        self.element = Element()
        self.effect = Effect()
        

    def findTag(self, root):
        for node in root:
            tag = node.tag.split("}")[1]
            if tag == "g":
                return node
        return ""


    def testIfGtypeIsDifferentFromGroup(self):
        self.document = self.effect.parse("arquivos_test/clones.svg")
        self.node = self.effect.document.getroot()
        self.g = G("arc", self.findTag(self.node), "ctx")
        self.x = self.g.attr("groupmode", "inkscape") or "group"
        self.assertTrue("group" != self.x)
      
    def testIfGtypeIsEqualToGroup(self):
        self.document = self.effect.parse("arquivos_test/arquivoErrado.svg")
        self.node = self.effect.document.getroot()
        self.g = G("arc", self.findTag(self.node), "ctx")
        print self.g.attr("groupmode", "inkscape") or "group"
        #self.assertTrue("group" == self.x)   
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()