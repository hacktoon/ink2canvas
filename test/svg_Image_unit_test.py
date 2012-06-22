import sys
import unittest

sys.path.append('..')

from inkex import Effect
from ink2canvas.canvas import Canvas
from ink2canvas.svg.Image  import Image

class TestSvg_image_unit_test(unittest.TestCase):


    def setUp(self):
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/svg_image_unit_test.svg")
        root = self.effect.document.getroot()   
        self.node = self.findTag(root, "g")
        self.node = self.findTag(self.node, "image")    
        self.canvas = Canvas(0, 0)
        self.image = Image(None, self.node, self.canvas, None);
        
    def findTag(self, root, no):
        for node in root:
            tag = node.tag.split("}")[1]
            if tag == no:
                return node
        return ""   
    
    def testGet_Data(self):
        x, y, weight, height, href = self.image.get_data()
        href = href[-12:]
        array = [x ,y, weight, height, href]
        imageArray = [97.285713, 255.6479, 554, 422, "5_images.jpg"]
        self.assertEqual(array, imageArray)
        
if __name__ == '__main__':
    unittest.main()      