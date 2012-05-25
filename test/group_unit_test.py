import sys
import unittest
from inkex import Effect
from ink2canvas.main import Ink2Canvas
sys.path.append('..')


class Test(unittest.TestCase):
    def setUp(self):
        self.ink2canvasGrouped = Ink2Canvas()
        file2 = "arquivos_test/group_unit_test_grouped.svg"
        self.ink2canvasGrouped.parse(file2)
        self.ink2canvasGrouped.effect()

        self.ink2canvasGroupedEdited = Ink2Canvas()
        file3 = "arquivos_test/group_unit_test_grouped_edited.svg"
        self.ink2canvasGroupedEdited.parse(file3)
        self.ink2canvasGroupedEdited.effect()

    def testCompareUngroupedAndGroupedEquals(self):
        self.assertEquals(self.ink2canvasGroupedEdited.core.canvas.output(), 
                          self.ink2canvasGrouped.core.canvas.output())
        


        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()