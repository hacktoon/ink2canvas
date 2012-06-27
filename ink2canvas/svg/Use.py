from ink2canvas.svg.AbstractShape import AbstractShape

class Use(AbstractShape):
    
    def drawClone(self):
        drawables = self.rootTree.getDrawable()
        OriginName = self.getCloneId()
        OriginObject = self.rootTree.buscaElementoPorId(OriginName,drawables)
        OriginObject.runDraw()
      
    def draw(self, isClip=False):
        if self.hasTransform():
            trans_matrix = self.getTransform()
            self.canvasContext.transform(*trans_matrix)
        self.drawClone()
        
    def getCloneId(self):
        return self.attr("href","xlink")[1:]