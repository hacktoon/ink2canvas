from ink2canvas.svg.AbstractShape import AbstractShape

class Image(AbstractShape):

    def get_data(self):
        x = self.attr("x")
        y = self.attr("y")
        width = self.attr("width")
        height = self.attr("height")
        href = self.attr("href","xlink")
        return x, y, width, height, href
    
    def draw(self, isClip=False):
        if self.has_transform():
            trans_matrix = self.get_transform()
            self.ctx.transform(*trans_matrix) # unpacks argument list
        if not isClip:
            style = self.get_style()
            self.set_style(style)
            self.ctx.beginPath()

        x, y, width, height, href = self.get_data()
        
        self.ctx.write("\n\tvar image = new Image();")
        self.ctx.write("\n\timage.src = '" + href +"';")
        self.ctx.write("\n\tctx.drawImage(image, %f,%f,%f,%f);" %(x,y,width, height))
        
        if not isClip: 
            self.ctx.closePath()
        
        


