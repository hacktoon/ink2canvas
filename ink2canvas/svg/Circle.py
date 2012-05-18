from ink2canvas.svg.AbstractShape import AbstractShape

class Circle(AbstractShape):
    def __init__(self, command, node, ctx, rootTree):
        AbstractShape.__init__(self, command, node, ctx, rootTree)
        #Nota: Daniel/Gustavo - modificamos AbstractShape(self, command, node, ctx) 
        #porque achamos que estava errado!
        self.command = "arc"

    def get_data(self):
        import math
        cx = self.attr("cx")
        cy = self.attr("cy")
        r = self.attr("r")
        return cx, cy, r, 0, math.pi * 2, True