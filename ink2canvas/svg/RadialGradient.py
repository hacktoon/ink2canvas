from ink2canvas.svg.Defs import Defs

class Radialgradient(Defs):
    def __init__(self, command, node, canvasContext, root):
        Defs.__init__(self, command, node, canvasContext, root)
        self.colorStops = []
        self.cx= 0
        self.cy= 0
        self.fx= 0
        self.fy= 0
        self.r = 0
    
    def setColorStops(self, colorStops):
        self.colorStops = colorStops
    
    def getData(self):
        cx = self.attr("cx")
        cy = self.attr("cy")
        fx = self.attr("fx")    
        fy = self.attr("fy")
        r = self.attr("r")
        return (cx, cy, fx, fy, r)

    def draw(self):
        pass