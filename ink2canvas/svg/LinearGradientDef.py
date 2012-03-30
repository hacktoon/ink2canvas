from ink2canvas.svg.GradientDef import GradientDef

class LinearGradientDef(GradientDef):
    def get_data(self):
        x1 = self.attr("x1")
        y1 = self.attr("y1")
        x2 = self.attr("x2")
        y2 = self.attr("y2")
        #self.createLinearGradient(href, x1, y1, x2, y2)

    def draw(self):
        pass