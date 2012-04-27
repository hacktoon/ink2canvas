import sys
import unittest
import inkex


sys.path.append('..')
import Canvas


class TestSequenceFunctions(unittest.TestCase):
    
    
    
    
    
    def testParse(self):
       
    
    
    def setUp(self):
        self.canvas = Canvas()
        self.canvas.code = ""
        self.string_rgb = "FFBBAA"
        self.rgb = [251, 186, 10]

    def test_out(self):
        text = 'ctx = canvas.getContext("2d");'
        self.canvas.out(text)
        self.assertTrue(self.canvas.code, text)

    def test_rgb(self):
        r, g, b = self.canvas.rgb(self.string_rgb)
        self.assertTrue(r, self.rgb[0])
        self.assertTrue(g, self.rgb[1])
        self.assertTrue(b, self.rgb[2])

    def test_style_for_stroke_width(self):
        dictionary = {"stroke-width":"3"}
        self.canvas.set_style(dictionary)
        self.assertTrue(self.canvas.code, "ctx.lineWidth = 3;")

    def test_style_for_stroke_linecap(self):
        dictionary = {"stroke-linecap":3}
        self.canvas.set_style(dictionary)
        self.assertTrue(self.canvas.code, "ctx.lineCap = 3;")

    def test_style_for_stroke_linejoin(self):
        dictionary = {"stroke-linejoin":3}
        self.canvas.set_style(dictionary)
        self.assertTrue(self.canvas.code, "ctx.lineJoin = 3;")
        
    def test_style_for_stroke_miterlimit(self):
        dictionary = {"stroke-miterlimit":3}
        self.canvas.set_style(dictionary)
        self.assertTrue(self.canvas.code, "ctx.miterLimit = 3;")

    def test_style_for_opacity(self):
        dictionary = {"opacity":0.5}
        self.canvas.set_style(dictionary)
        self.assertTrue(self.canvas.code, "ctx.globalAlpha = 3;")
        
    def test_style_for_stroke(self):
        r, g, b = self.rgb
        dictionary = {"stroke":self.string_rgb}
        self.canvas.set_style(dictionary)
        self.assertTrue(self.canvas.code, "ctx.strokeStyle = 'rgb(%d, %d, %d)';" % (r, g, b))

    def test_style_for_stroke_with_opacity(self):
        r, g, b = self.rgb
        dictionary = {"stroke":self.string_rgb, "fill-opacity": 0}
        self.canvas.set_style(dictionary)
        self.assertTrue(self.canvas.code, "ctx.strokeStyle = 'rgba(%d, %d, %d, %d)';" % (r, g, b, 0))

if __name__ == '__main__':
    unittest.main()
