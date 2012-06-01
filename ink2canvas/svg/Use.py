from ink2canvas.svg.AbstractShape import AbstractShape

class Use(AbstractShape):
    
    def drawClone(self):
        drawables = self.rootTree.getDrawable()
        OriginName = self.getCloneId()
        OriginObject = self.rootTree.buscaElementoPorId(OriginName,drawables)
        OriginObject.draw()
#        self.ctx.closePath();
      
    def draw(self, isClip=False):
        if self.has_transform():
            trans_matrix = self.get_transform()
            self.ctx.transform(*trans_matrix)
        self.drawClone()
        
    def getCloneId(self):
        return self.attr("href","xlink")[1:]