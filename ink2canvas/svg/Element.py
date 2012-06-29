from ink2canvas.lib import inkex

class Element:
    def __init__(self):
        self.children = []
        self.parent = None
        
    def setParent(self, parent):
        self.parent = parent
    
    def getParent(self):
        return self.parent
    
    def getChildren(self):
        return self.children
    
    def addChild(self, child):
        self.children.append(child)
        
    def initDraw(self):
        pass
    
    def draw(self):
        pass
    
    def endDraw(self):
        pass
    
    def drawClip(self):
        pass
    
    def runDraw(self, isClip = False):
        self.initDraw()
        if self.hasClip():
            self.drawClip()        
        self.draw(isClip)
        for child in self.children:
            child.runDraw()
        self.endDraw()
    
    def hasClip(self):
        return bool(self.attr("clip-path"))
    
    def attr(self, val, ns=""):
        if ns:
            val = inkex.addNS(val, ns)
        try:
            attr = float(self.node.get(val))
        except:
            attr = self.node.get(val)
        return attr