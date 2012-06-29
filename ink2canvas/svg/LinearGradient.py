from ink2canvas.svg.Defs import Defs

class Lineargradient(Defs):
    def __init__(self, command, node, canvasContext, root):
        Defs.__init__(self, command, node, canvasContext, root)
        self.colorStops = {}
        self.link = None
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        
    def setColorStops(self, colorStops):
        self.colorStops = colorStops
    
    def getData(self):
        x1 = self.attr("x1")
        y1 = self.attr("y1")
        x2 = self.attr("x2")
        y2 = self.attr("y2")
        return (x1, y1, x2, y2)