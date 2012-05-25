from ink2canvas.svg.Defs import Defs
from ink2canvas.svg.GradientDef import GradientDef
from numpy.ma.core import get_data

class LinearGradient(Defs):
    def __init__(self, command, node, ctx, root):
        Defs.__init__(self, command, node, ctx, root)
        self.colorStops = []
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        
    def setColorStops(self, colorStops):
        self.colorStops = colorStops
    
#    def createLinearGradient(self):
#        x1, y1, x2, y2 = self.gradient.get_data()
#        self.ctx.createLinearGradient("grad", x1, y1, x2, y2)
#        for stop in self.gradient.stops:
#            color = self.ctx.getColor(stop.split(";")[0].split(":")[1] , stop.split(";")[1].split(":")[1])
#            offset = float(stop.split(";")[2].split(":")[1])
#            self.ctx.addColorStop("grad", offset, color)
    
    def get_data(self):
        x1 = self.attr("x1")
        y1 = self.attr("y1")
        x2 = self.attr("x2")
        y2 = self.attr("y2")
        return (x1, y1, x2, y2)