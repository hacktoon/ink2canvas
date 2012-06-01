from ink2canvas.svg.Defs import Defs
from ink2canvas.svg.GradientDef import GradientDef

class Radialgradient(Defs):
    def __init__(self, command, node, ctx, root):
        Defs.__init__(self, command, node, ctx, root)
        self.colorStops = []
        self.cx= 0
        self.cy= 0
        self.fx= 0
        self.fy= 0
        self.r = 0
    
    def get_data(self):
        cx = self.attr("cx")
        cy = self.attr("cy")
        fx = self.attr("fx")    
        fy = self.attr("fy")
        r = self.attr("r")
        return (cx, cy, fx, fy, r)

    def draw(self):
        pass