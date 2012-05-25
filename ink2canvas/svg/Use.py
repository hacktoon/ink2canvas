from ink2canvas.svg.AbstractShape import AbstractShape

class Use(AbstractShape):
    def get_data(self):
        x = self.attr("x")
        y = self.attr("y")
        return x, y
    def draw(self, isClip=False):
        pass
    
    def getCloneId(self):
        return self.attr("href","xlink")[1:]