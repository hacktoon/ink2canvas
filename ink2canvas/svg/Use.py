from ink2canvas.svg.AbstractShape import AbstractShape

class Use(AbstractShape):
    
    def drawClone(self):
        drawables = self.rootTree.getDrawable()
        OriginName = self.getCloneId()
        OriginObject = self.rootTree.searchElementById(OriginName,drawables)
        OriginObject.runDraw()
      
    def draw(self, isClip=False):
        if self.hasTransform():
            transMatrix = self.getTransform()
            self.canvasContext.transform(*transMatrix)
        self.drawClone()
        
    def getCloneId(self):
        return self.attr("href","xlink")[1:]