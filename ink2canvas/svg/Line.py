from ink2canvas.svg.Path import Path

class Line(Path):
    def getData(self):
        x1 = self.attr("x1")
        y1 = self.attr("y1")
        x2 = self.attr("x2")
        y2 = self.attr("y2")
        return (("M", (x1, y1)), ("L", (x2, y2)))