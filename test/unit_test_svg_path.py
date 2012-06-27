import sys
import unittest
from inkex import Effect
sys.path.append('..')

from ink2canvas.canvas import Canvas
from ink2canvas.svg.Path import Path

class TestSvgPath(unittest.TestCase):
    def setUp(self):
        self.effect = Effect()
        self.document = self.effect.parse("arquivos_test/unit_test_svg_path.svg")
        root = self.effect.document.getroot()   
        self.node = self.findTag(root, "g")
        self.node = self.findTag(self.node, "path")    
        self.canvas = Canvas(0, 0)
        '''Fictional data used in methods such as pathlineto, pathcurveto, pathmoveto, patharcto. we made it so that
        the 5th parameters (600) is larger then the others, guaranteeing this way that the sqrt value is not a negative
        value in patharcto.'''
        self.data =[1.0, 2.0, 3.0, 4.0, 5.0, 600.0, 7.0]
        self.path = Path(None, self.node, self.canvas, None)
        
    def findTag(self, root, no):
        for node in root:
            tag = node.tag.split("}")[1]
            if tag == no:
                return node
        return ""   
    
    def testGetData(self):
        vetor = self.path.getData()
        vetorDaElipse = [['M', [447.49757, 166.4584]], ['A', [197.48482, 67.680222, 0.0, 1, 1, 52.527939, 166.4584]], ['A', [197.48482, 67.680222, 0.0, 1, 1, 447.49757, 166.4584]], ['Z', []]]
        self.assertEqual(vetor, vetorDaElipse)
        
    def testPathMoveTo(self):
        self.path.pathMoveTo(self.data)
        self.assertEqual(self.path.canvasContext.code, ['\tctx.moveTo(1.000000, 2.000000);\n'])

        
    def testPathLineTo(self):
        self.path.pathLineTo(self.data)
        self.assertEqual(self.path.canvasContext.code, ['\tctx.lineTo(1.000000, 2.000000);\n'])
        
    def testPathCurveTo(self):
        self.path.pathCurveTo(self.data)
        self.assertEqual(self.path.canvasContext.code, ['\tctx.bezierCurveTo(1.000000, 2.000000, 3.000000, 4.000000, 5.000000, 600.000000);\n'])
        
    def testPathArcTo(self):         
        self.path.currentPosition = [600.0, 7.0]
        self.path.pathArcTo(self.data)
        self.assertEqual(self.path.canvasContext.code, [])
        self.path.currentPosition = [0.25, 0.25]
        self.path.pathArcTo(self.data)
        self.assertEqual(self.path.canvasContext.code, ['\tctx.translate(300.125000, 3.625000);\n', '\tctx.rotate(0.052360);\n', '\tctx.scale(0.500000, 1.000000);\n', '\tctx.arc(0.000000, 0.000000, 599.408034, 3.121031, 6.26262379, -4);\n', '\tctx.scale(2.000000, 1.000000);\n', '\tctx.rotate(-0.052360);\n', '\tctx.translate(-300.125000, -3.625000);\n'])

    def testDraw(self):
        self.maxDiff = None
        self.path.draw(False)
        self.assertEqual(self.path.canvasContext.code, ["\tctx.lineJoin = 'miter';\n", "\tctx.strokeStyle = 'rgb(0, 0, 0)';\n", "\tctx.lineCap = 'butt';\n", '\tctx.lineWidth = 1.000000;\n', "\tctx.fillStyle = 'rgb(255, 0, 0)';\n", '\tctx.beginPath();\n', '\tctx.transform(0.707107, -0.707107, 0.707107, 0.707107, -44.476826, 225.540250);\n', '\tctx.moveTo(447.497570, 166.458400);\n', '\tctx.translate(250.012754, 166.472848);\n', '\tctx.rotate(0.000000);\n', '\tctx.scale(1.000000, 0.342711);\n', '\tctx.arc(0.000000, 0.000000, 197.484820, -0.000213, 3.14180613, 0);\n', '\tctx.scale(1.000000, 2.917910);\n', '\tctx.rotate(-0.000000);\n', '\tctx.translate(-250.012754, -166.472848);\n', '\tctx.translate(250.012754, 166.443952);\n', '\tctx.rotate(0.000000);\n', '\tctx.scale(1.000000, 0.342711);\n', '\tctx.arc(0.000000, 0.000000, 197.484820, 3.141379, 6.28339879, 0);\n', '\tctx.scale(1.000000, 2.917910);\n', '\tctx.rotate(-0.000000);\n', '\tctx.translate(-250.012754, -166.443952);\n', '\tctx.closePath();\n', '\tctx.fill();\n', '\tctx.stroke();\n'])
       
if __name__ == '__main__':
    unittest.main()

