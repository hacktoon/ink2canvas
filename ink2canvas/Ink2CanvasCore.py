import svg
from canvas import Canvas

class Ink2CanvasCore(): 
    
    def __init__(self, inkex, effect):
        self.inkex = inkex
        self.canvas = None
        self.effect = effect
    
    def drawClone(self, childNode, element):
        cloneNode = self.getCloneNode(childNode)
        if (element.has_transform()):
            transMatrix = element.get_transform()
            self.canvas.transform(*transMatrix)
        self.walkInSVGNodes([cloneNode])

    def drawGradient(self, element):
        gradient = self.getGradientDef(element)
        element.start(gradient)

    def drawClip(self, element):
        clipPath = self.getClipDef(element)
        self.canvas.beginPath()
        if (element.has_transform()):
            self.canvas.save()
            transMatrix = element.get_transform()
            self.canvas.transform(*transMatrix)
        self.walkInSVGNodes(clipPath, True)
        if (element.has_transform()):
            self.canvas.restore()
        self.canvas.clip()

    def walkInSVGNodes(self, rootNode, isClip=False):
        for childNode in rootNode:
            tagName = self.getNodeTagName(childNode)
            className = tagName.capitalize()

            #if there's not an implemented class, continues
            if not hasattr(svg, className):
                continue
            # creates a instance of 'element'
            # similar to 'element = Rect(tagName, childNode, ctx)'
            element = getattr(svg, className)(tagName, childNode, self.canvas)
            
            if self.isCloneNode(childNode):
                self.drawClone(childNode, element)
                continue
            
            self.drawGradient(element)
               
            if not isClip and element.has_clip():
                self.drawClip(element)
            
            #clipping elements are drawn differently
            element.draw(isClip)
            self.walkInSVGNodes(childNode, isClip)
            element.end()

    def getNodeTagName(self, node):
        # remove namespace part from "{http://www.w3.org/2000/svg}elem"
        return node.tag.split("}")[1]
    
    def getGradientDef(self, elem):
        if not elem.has_gradient():
            return None
        gradientHref = elem.get_gradient_href()
        
        # get the gradient element
        gradient = self.effect.xpathSingle("//*[@id='%s']" % gradientHref)
        
        # get the color stops
        colorStops = gradient.get(self.inkex.addNS("href", "xlink"))      
        colorStopsNodes = self.effect.xpathSingle("//svg:linearGradient[@id='%s']" % colorStops[1:])
        colors = []
        for color in colorStopsNodes:
            colors.append(color.get("style")+"offset:"+color.get("offset"))
        if gradient.get("r"):
            return svg.RadialGradientDef(gradient, colors)
        else:
            return svg.LinearGradientDef(gradient, colors)
        
    def getClipDef(self, elem):
        clipId = elem.get_clip_href()
        return self.xpathSingle("//*[@id='%s']" % clipId)

    def isCloneNode(self, node):
        cloneHref = node.get(self.inkex.addNS("cloneHref", "xlink"))
        return bool(cloneHref)  
    
    def getCloneNode(self, node):
        cloneHref = node.get(self.inkex.addNS("cloneHref", "xlink"))
        clone = self.xpathSingle("//*[@id='%s']" % cloneHref[1:])
        return clone

    def effect(self):
        svgRoot = self.document.getroot()
        width = self.inkex.unittouu(svgRoot.get("width"))
        height = self.inkex.unittouu(svgRoot.get("height"))
        self.canvas = Canvas(width, height)
        self.walkInSVGNodes(svgRoot)  
    