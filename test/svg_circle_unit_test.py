import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.svg.Circle import Circle

    #Nota: O inkscape nao gera imagens com o tag circle.
    #Ao inves, gera com o tag g->path->arc
    #Entao para o ink2canvas a funcao circle pode ser inutil   

class TestSvgCircle(unittest.TestCase):
    def setUp(self):
        self.circle = Circle(12, 12, 12)
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/CirculoVerdadeiro.svg")
        root = self.effect.document.getroot()
        
        for node in root:
            tag = node.tag.split("}")[1]
            if(tag == 'circle'):
                self.node = node
                break
 
    def testGet_Data_Cx(self):
        self.circle.node = self.node
        retCx, retCy, retR , zero, DoisPi, OpostoDeFalse = self.circle.get_data()
        self.assertEqual(retCx, 600)
        
    def testGet_Data_Cy(self):
        self.circle.node = self.node
        retCx, retCy, retR , zero, DoisPi, OpostoDeFalse = self.circle.get_data()
        self.assertEqual(retCy, 200)
        
    def testGet_Data_R(self):
        self.circle.node = self.node
        retCx, retCy, retR , zero, DoisPi, OpostoDeFalse = self.circle.get_data()
        self.assertEqual(retR, 100)

if __name__ == '__main__':
    unittest.main()

