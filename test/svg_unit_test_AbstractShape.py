import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.AbstractShape import AbstractShape
from ink2canvas.svg.Element import Element

from ink2canvas.canvas import Canvas


class TestSvgAbstractShape(unittest.TestCase):
    
    def returnsGnode(self, root):
        for node in root:
            tag = node.tag.split("}")[1]
            if tag == "path":
                return node
        return None
    
    
    
    
    def setUp(self):
        self.canvas = Canvas(0,0)
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/circulo.svg")
        print self.document
        self.root = self.effect.document.getroot()
        print self.root
        self.node = self.returnsGnode(self.root)
        print self.node
        self.abstractShape = AbstractShape( None,self.node,self.canvas)   
   
        print self.abstractShape.get_style()
        
    def testX(self):
        
        self.abstractShape.node = self.node
        self.abstractShape.command = "arc"
        
        print self.abstractShape.get_style()
        print "olaaa" 

if __name__ == '__main__':
    unittest.main()