from ink2canvas.svg.Defs import Defs
from ink2canvas.svg.GradientDef import GradientDef

class Radialgradient(Defs):
    def __init__(self, command, node, ctx):
        Defs.__init__(self, command, node, ctx)
    
    def get_data(self):
        cx = self.attr("cx")
        cy = self.attr("cy")
        fx = self.attr("fx")    
        fy = self.attr("fy")
        r = self.attr("r")
        return (cx, cy, fx, fy, r)

    def draw(self):
        pass