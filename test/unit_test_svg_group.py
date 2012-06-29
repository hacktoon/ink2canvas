import sys
import unittest

sys.path.append('..')
from ink2canvas.main import Ink2Canvas


class TestSvgGroup(unittest.TestCase):
    def setUp(self):
        self.ink2canvasGrouped = Ink2Canvas()
        file2 = "TestFiles/unit_test_group_grouped.svg"
        self.ink2canvasGrouped.parse(file2)
        self.ink2canvasGrouped.effect()

        self.ink2canvasGroupedEdited = Ink2Canvas()
        file3 = "TestFiles/unit_test_group_grouped_edited.svg"
        self.ink2canvasGroupedEdited.parse(file3)
        self.ink2canvasGroupedEdited.effect()

    def testCompareUngroupedAndGroupedEquals(self):
        self.assertEquals(self.ink2canvasGroupedEdited.core.canvas.output(), 
                          self.ink2canvasGrouped.core.canvas.output())
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()