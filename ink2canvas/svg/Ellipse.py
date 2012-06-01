from ink2canvas.svg.AbstractShape import AbstractShape

class Ellipse(AbstractShape):
    def get_data(self):
        cx = self.attr("cx")
        cy = self.attr("cy")
        rx = self.attr("rx")
        ry = self.attr("ry")
        return cx, cy, rx, ry

    def draw(self, isClip=False):
        import math
        cx, cy, rx, ry = self.get_data()
        if not isClip:
            style = self.get_style()
            self.set_style(style)
            self.ctx.beginPath()
        if self.has_transform():
            trans_matrix = self.get_transform()
            self.ctx.transform(*trans_matrix) # unpacks argument list

        KAPPA = 4 * ((math.sqrt(2) - 1) / 3)
        self.ctx.moveTo(cx, cy - ry)
        self.ctx.bezierCurveTo(cx + (KAPPA * rx), cy - ry,  cx + rx, cy - (KAPPA * ry), cx + rx, cy)
        self.ctx.bezierCurveTo(cx + rx, cy + (KAPPA * ry), cx + (KAPPA * rx), cy + ry, cx, cy + ry)
        self.ctx.bezierCurveTo(cx - (KAPPA * rx), cy + ry, cx - rx, cy + (KAPPA * ry), cx - rx, cy)
        self.ctx.bezierCurveTo(cx - rx, cy - (KAPPA * ry), cx - (KAPPA * rx), cy - ry, cx, cy - ry)
        
        self.set_gradient()

        
        if not isClip:
            self.ctx.closePath()