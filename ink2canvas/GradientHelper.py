from ink2canvas.lib.simpletransform import parseTransform

class GradientHelper(object):
    
    def __init__(self, abstractShape):
        self.abstractShape = abstractShape
      
    def hasGradient(self, key):
        style = self.abstractShape.getStyle()
        
        if key in style:
            styleParamater = style[key]
            if styleParamater.startswith("url(#linear"):
                return "linear"
            if styleParamater.startswith("url(#radial"):
                return "radial"
        return None

    def getGradientHref(self, key):
        style = self.abstractShape.getStyle()
        if key in style:
            return style[key][5:-1]
        return
      
    def setGradientFill(self):
        gradType = self.hasGradient("fill")
        if (gradType):
            gradient = self.setComponentGradient("fill", gradType)
            self.abstractShape.canvasContext.setFill("gradient=grad")           
            if(self.hasGradientTransform(gradient)):
                self.abstractShape.canvasContext.fill();
                self.abstractShape.canvasContext.restore()
                return True
            
    def setGradientStroke(self):   
        gradType = self.hasGradient("stroke")
        if (gradType):
            gradient = self.setComponentGradient("stroke", gradType)
            self.abstractShape.canvasContext.setStroke("gradient=grad")
            if(self.hasGradientTransform(gradient)):
                self.abstractShape.canvasContext.stroke();
                self.abstractShape.canvasContext.restore()
                return True
            
    def hasGradientTransform(self, gradient):
        return bool(gradient.attr("gradientTransform"))
    
    def setGradientTransform(self, gradient):
        dataString = gradient.attr("gradientTransform")
        dataMatrix = parseTransform(dataString)
        m11, m21, dx = dataMatrix[0]
        m12, m22, dy = dataMatrix[1]
        self.abstractShape.canvasContext.transform(m11, m12, m21, m22, dx, dy)
            
    def setComponentGradient(self, key, gradType):
        gradientId = self.getGradientHref(key)
        if(gradType == "linear"):
            gradient = self.abstractShape.rootTree.getLinearGradient(gradientId)
        if(gradType == "radial"):
            gradient = self.abstractShape.rootTree.getRadialGradient(gradientId)
        
        if(gradient.link != None):
            gradient.colorStops = self.abstractShape.rootTree.getLinearGradient(gradient.link).colorStops
            
        if(self.hasGradientTransform(gradient)):
            self.abstractShape.canvasContext.save()
            self.setGradientTransform(gradient)    
            
        if(gradType == "linear"):
            x1, y1, x2, y2 = gradient.getData()
            self.abstractShape.canvasContext.createLinearGradient("grad", x1, y1, x2, y2)
        if(gradType == "radial"):
            cx, cy, fx, fy, r = gradient.getData()
            self.abstractShape.canvasContext.createRadialGradient("grad", cx, cy, 0, fx, fy, r)
            
        for stopKey, stopValue in gradient.colorStops.iteritems():
            offset = float(stopKey)
            color = self.abstractShape.canvasContext.getColor(stopValue.split(";")[0].split(":")[1] , stopValue.split(";")[1].split(":")[1] )
            self.abstractShape.canvasContext.addColorStop("grad", offset, color)

        return gradient
    
    def createLinearGradient(self):
        x1, y1, x2, y2 = self.gradient.getData()
        self.abstractShape.canvasContext.createLinearGradient("grad", x1, y1, x2, y2)
        for stop in self.gradient.stops:
            color = self.canvasContext.getColor(stop.split(";")[0].split(":")[1] , stop.split(";")[1].split(":")[1])
            offset = float(stop.split(";")[2].split(":")[1])
            self.abstractShape.canvasContext.addColorStop("grad", offset, color)    