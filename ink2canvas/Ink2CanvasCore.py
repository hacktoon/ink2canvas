import svg
from ink2canvas.svg.ClipPath import Clippath
from ink2canvas.svg.RadialGradient import Radialgradient
from ink2canvas.svg.LinearGradient import Lineargradient
from ink2canvas.svg import Root, Defs

class Ink2CanvasCore(): 
    
    def __init__(self, inkex, effect):
        self.inkex = inkex
        self.canvas = None
        self.effect = effect
        self.root = Root()
        
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
        colorStops = {}
        for stop in tag:
            colorStops[stop.get("offset")] = stop.get("style")
        radialGrad = Radialgradient(None, tag, self.canvas, self.root)
        radialGrad.setColorStops(colorStops)
        self.root.addChildRadialGradient(radialGrad.attr("id"), radialGrad)
        if(radialGrad.attr("href","xlink") != None):
            radialGrad.link = radialGrad.attr("href","xlink")[1:]
    
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
        return node.tag.split("}")[1]
