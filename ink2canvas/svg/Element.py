from ink2canvas.lib import inkex

class Element:
    def __init__(self):
        self.children = []
        self.isClip = False
        
    def setIsClip(self, value):
        self.isClip = value
    
    def getIsClip(self):
        return self.isClip   
    
    def setParent(self, parent):
        self.parent = parent
    
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
    
    def runDraw(self):
        self.initDraw()
        self.draw()
        for child in self.children:
            if child.getIsClip() == False:
                child.runDraw()
        self.endDraw()
    
    def attr(self, val, ns=""):
        if ns:
            val = inkex.addNS(val, ns)
        try:
            attr = float(self.node.get(val))
        except:
            attr = self.node.get(val)
        return attr