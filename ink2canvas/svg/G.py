from ink2canvas.svg.AbstractShape import AbstractShape

class G(AbstractShape):       
        
    def draw(self, isClip=False):
        #get layer label, if exists
        gtype = self.attr("groupmode", "inkscape") or "group"
        if self.hasTransform():
            transMatrix = self.getTransform()
            self.canvasContext.transform(*transMatrix)