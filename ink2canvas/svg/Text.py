from ink2canvas.svg.AbstractShape import AbstractShape

class Text(AbstractShape):
    def textHelper(self, tspan):
        val = ""
        if tspan.text:
            val += tspan.text
        for ts in tspan:
            val += self.textHelper(ts)
        if tspan.tail:
            val += tspan.tail
        return val

    def setTextStyle(self, style):
        keys = ("font-style", "font-weight", "font-size", "font-family")
        text = []
        for key in keys:
            if key in style:
                text.append(style[key])
        self.canvasContext.setFont(" ".join(text))

    def getData(self):
        x = self.attr("x")
        y = self.attr("y")
        return x, y

    def draw(self, isClip=False):
        x, y = self.getData()
        style = self.getStyle()
        if self.hasTransform():
            transMatrix = self.getTransform()
            self.canvasContext.transform(*transMatrix) # unpacks argument list
        self.setStyle(style)
        self.setTextStyle(style)

        for tspan in self.node:
            text = self.textHelper(tspan)
            _x = float(tspan.get("x"))
            _y = float(tspan.get("y"))
            self.canvasContext.fillText(text, _x, _y)
        
        self.gradientHelper.setGradientFill()
        self.gradientHelper.setGradientStroke()
