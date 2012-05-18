from ink2canvas.svg.AbstractShape import AbstractShape

class G(AbstractShape):       
        
    def draw(self, isClip=False):
        #get layer label, if exists
        gtype = self.attr("groupmode", "inkscape") or "group"
        if self.has_transform():
            trans_matrix = self.get_transform()
            self.ctx.transform(*trans_matrix)