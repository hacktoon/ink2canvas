from ink2canvas.svg.GradientDef import GradientDef

class RadialGradientDef(GradientDef):
    def get_data(self):
        cx = self.attr("cx")
        cy = self.attr("cy")
        r = self.attr("r")
        #self.createRadialGradient(href, cx, cy, r, cx, cy, r)

    def draw(self):
        pass