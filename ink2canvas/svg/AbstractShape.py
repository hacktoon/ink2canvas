from ink2canvas.svg.Element import Element
from ink2canvas.lib import simplestyle
from ink2canvas.lib.simpletransform import parseTransform
from ink2canvas.GradientHelper import GradientHelper

class AbstractShape(Element):
    def __init__(self, command, node, canvasContext, rootTree):
        Element.__init__(self)
        self.node = node
        self.command = command
        self.canvasContext = canvasContext
        self.rootTree = rootTree
        self.gradientHelper = GradientHelper(self)

    def getId(self):
        return self.attr("id")    
    
    def getData(self):
        return

    def getStyle(self):
        style = simplestyle.parseStyle(self.attr("style"))
        if style == {}:
            parent = self.getParent()
            while (parent != None and style == {}):
                style = simplestyle.parseStyle(parent.attr("style"))
                parent = parent.getParent()        
        
        #remove any trailing space in dict keys/values
        style = dict([(str.strip(k), str.strip(v)) for k,v in style.items()])
        return style

    def setStyle(self, style):
        """Translates style properties names into method calls"""
        self.canvasContext.style = style
        for key in style:
            tmp_list = map(str.capitalize, key.split("-"))
            method = "set" + "".join(tmp_list)
            if hasattr(self.canvasContext, method) and style[key] != "none":
                getattr(self.canvasContext, method)(style[key])
        #saves style to compare in next iteration
        self.canvasContext.style_cache = style

    def hasTransform(self):
        return bool(self.attr("transform"))

    def getTransform(self):
        data = self.node.get("transform")
        if not data:
            return
        matrix = parseTransform(data)
        m11, m21, dx = matrix[0]
        m12, m22, dy = matrix[1]
        return m11, m12, m21, m22, dx, dy   

    def getClipId(self):
        return self.attr("clip-path")[5:-1]

    def initDraw(self):
        self.canvasContext.write("\n// #%s" % self.attr("id"))
        if self.hasTransform() or self.hasClip():
            self.canvasContext.save()
        
    def draw(self, isClip=False):
        data = self.getData()
        if self.hasTransform():
            transMatrix = self.getTransform()
            self.canvasContext.transform(*transMatrix)
            
        if not isClip:
            style = self.getStyle()
            self.setStyle(style)
            self.canvasContext.beginPath()       
                
        getattr(self.canvasContext, self.command)(*data)

        gradientFill = self.gradientHelper.setGradientFill()
        gradientStroke = self.gradientHelper.setGradientStroke()
        
        if not isClip: 
            self.canvasContext.closePath()
            if(not gradientFill):        
                self.canvasContext.fill()
            if(not gradientStroke):
                self.canvasContext.stroke()

    def drawClip(self):
        clipId = self.getClipId()
        elementClip = self.rootTree.getClipPath(clipId)
        self.canvasContext.beginPath()
        if (self.hasTransform()):
            self.canvasContext.save()
            transMatrix = self.getTransform()
            self.canvasContext.transform(*transMatrix)
        #DRAW
        elementClip.runDraw(True)
        if (self.hasTransform()):
            self.canvasContext.restore()
        self.canvasContext.clip()   

    def endDraw(self):
        if self.hasTransform() or self.hasClip():
            self.canvasContext.restore()