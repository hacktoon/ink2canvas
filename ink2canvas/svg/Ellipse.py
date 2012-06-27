from ink2canvas.svg.AbstractShape import AbstractShape

class Ellipse(AbstractShape):
    def getData(self):
        cx = self.attr("cx")
        cy = self.attr("cy")
        rx = self.attr("rx")
        ry = self.attr("ry")
        return cx, cy, rx, ry

    def draw(self, isClip=False):
        import math
        cx, cy, rx, ry = self.getData()
        if not isClip:
            style = self.getStyle()
            self.setStyle(style)
            self.canvasContext.beginPath()
        if self.hasTransform():
            trans_matrix = self.getTransform()
            self.canvasContext.transform(*trans_matrix) # unpacks argument list

        auxiliarNumber = 4 * ((math.sqrt(2) - 1) / 3)
        self.canvasContext.moveTo(cx, cy - ry)
        self.canvasContext.bezierCurveTo(cx + (auxiliarNumber * rx), cy - ry,  cx + rx, cy - (auxiliarNumber * ry), cx + rx, cy)
        self.canvasContext.bezierCurveTo(cx + rx, cy + (auxiliarNumber * ry), cx + (auxiliarNumber * rx), cy + ry, cx, cy + ry)
        self.canvasContext.bezierCurveTo(cx - (auxiliarNumber * rx), cy + ry, cx - rx, cy + (auxiliarNumber * ry), cx - rx, cy)
        self.canvasContext.bezierCurveTo(cx - rx, cy - (auxiliarNumber * ry), cx - (auxiliarNumber * rx), cy - ry, cx, cy - ry)

        gradientFill = self.gradientHelper.setGradientFill()
        gradientStroke = self.gradientHelper.setGradientStroke()
        
        if not isClip: 
            self.canvasContext.closePath()
            if(not gradientFill):        
                self.canvasContext.fill()
            if(not gradientStroke):
                self.canvasContext.stroke()
            