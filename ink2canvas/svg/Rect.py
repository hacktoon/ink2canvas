from ink2canvas.svg.AbstractShape import AbstractShape

class Rect(AbstractShape):
    def getData(self):
        x = self.attr("x")
        y = self.attr("y")
        w = self.attr("width")
        h = self.attr("height")
        rx = self.attr("rx") or 0
        ry = self.attr("ry") or 0
        return x, y, w, h, rx, ry