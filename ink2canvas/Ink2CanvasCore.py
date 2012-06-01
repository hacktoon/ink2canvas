import svg
from canvas import Canvas
from ink2canvas.svg.ClipPath import Clippath
from ink2canvas.svg.RadialGradient import Radialgradient
from ink2canvas.svg.LinearGradient import Lineargradient
from ink2canvas.svg import Root, LinearGradient, Defs ,G, Use
from ink2canvas.svg.Element import Element

class Ink2CanvasCore(): 
    
    def __init__(self, inkex, effect):
        self.inkex = inkex
        self.canvas = None
        self.effect = effect
        self.root = Root()
    
    
        
    def isClone(self):
        return isinstance(self, Use);
    
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
        #DRAW
        self.walkInSVGNodes(clipPath, True)
        if (element.has_transform()):
            self.canvas.restore()
        self.canvas.clip()

#    
    def createClipPathNode(self,element,tag):
        for subTag in tag:
            tagName = self.getNodeTagName(subTag)
            className = tagName.capitalize()

            #if there's not an implemented class, continues
            if not hasattr(svg, className):
                continue
            # creates a instance of 'element'
            tipoDoClip = getattr(svg, className)(tagName, subTag, self.canvas, self.root)

            self.root.addChildClipPath(element.attr("id"),tipoDoClip)
    
    def createLinearGradient(self,element,tag):
        colorStops = {}
        for stop in tag:
            colorStops[stop.get("offset")] = stop.get("style")
        linearGrad = Lineargradient(None, tag, self.canvas, self.root)
        linearGrad.setColorStops(colorStops)
        self.root.addChildLinearGradient(linearGrad.attr("id"), linearGrad)
        if(linearGrad.attr("href","xlink") != None):
            linearGrad.link = linearGrad.attr("href","xlink")[1:]
        
    def createRadialGradient(self,element,tag):
        pass
    
    def createDrawable(self,element,tag):
        for eachTag in tag:
            elementChild = self.createElement(eachTag)
            if(elementChild == None):
                continue
            elementChild.setParent(element)
            element.addChild(elementChild)
            self.createDrawable(elementChild, eachTag)
                
        
    def createModifiers(self,tag):
        for eachTag in tag:
            elementChild = self.createElement(eachTag)
            if(elementChild == None):
                continue
            if(isinstance(elementChild, Clippath)):
                self.createClipPathNode(elementChild,eachTag)
            else:
                if(isinstance(elementChild, Lineargradient)):
                    self.createLinearGradient(elementChild,eachTag)
                else:
                    if(isinstance(elementChild, Radialgradient)):
                        self.createRadialGradient(elementChild,eachTag)

    def createElement(self,tag):
        tagName = self.getNodeTagName(tag)
        className = tagName.capitalize()

        #if there's not an implemented class, continues
        if not hasattr(svg, className):
            return None
        # creates a instance of 'element'
        return  getattr(svg, className)(tagName, tag, self.canvas, self.root)

    def createTree(self,fileSVG):
        for tag in fileSVG:
            element = self.createElement(tag)
            if(element == None):
                continue
            if(isinstance(element, Defs)):
                self.createModifiers(tag)
            else:
                self.root.addChildDrawable(element)
                self.createDrawable(element,tag);
                        
            

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
            return svg.RadialGradient(gradient, colors)
        else:
            return svg.LinearGradient(gradient, colors)
        
    #MUDAR CLIP
    def getClipDef(self, elem):
        clipId = elem.getClipId()
        return self.xpathSingle("//*[@id='%s']" % clipId)

    def isCloneNode(self, node):
        cloneHref = node.get(self.inkex.addNS("cloneHref", "xlink"))
        return bool(cloneHref)  
    
    def getCloneNode(self, node):
        cloneHref = node.get(self.inkex.addNS("cloneHref", "xlink"))
        clone = self.xpathSingle("//*[@id='%s']" % cloneHref[1:])
        return clone
    