from ink2canvas.svg.Element import Element
from ink2canvas.lib import simplestyle
from ink2canvas.lib.simpletransform import parseTransform
from ink2canvas.svg.LinearGradient import Lineargradient

class AbstractShape(Element):
    def __init__(self, command, node, ctx, rootTree):
        Element.__init__(self)
        self.node = node
        self.command = command
        self.ctx = ctx
        self.rootTree = rootTree

    def get_data(self):
        return

    def get_style(self):
        style = simplestyle.parseStyle(self.attr("style"))
        #remove any trailing space in dict keys/values
        style = dict([(str.strip(k), str.strip(v)) for k,v in style.items()])
        return style

    def set_style(self, style):
        """Translates style properties names into method calls"""
        self.ctx.style = style
        for key in style:
            tmp_list = map(str.capitalize, key.split("-"))
            method = "set" + "".join(tmp_list)
            if hasattr(self.ctx, method) and style[key] != "none":
                getattr(self.ctx, method)(style[key])
        #saves style to compare in next iteration
        self.ctx.style_cache = style

    def has_transform(self):
        return bool(self.attr("transform"))

    def get_transform(self):
        data = self.node.get("transform")
        if not data:
            return
        matrix = parseTransform(data)
        m11, m21, dx = matrix[0]
        m12, m22, dy = matrix[1]
        return m11, m12, m21, m22, dx, dy

    def has_gradient(self):
        style = self.get_style()
        if "fill" in style:
            fill = style["fill"]
            return fill.startswith("url(#linear") or \
                   fill.startswith("url(#radial")
        return False

    def get_gradient_href(self):
        style = self.get_style()
        if "fill" in style:
            return style["fill"][5:-1]
        return

    def getClipId(self):
        return self.attr("clip-path")[5:-1]

    def initDraw(self):
        self.ctx.write("\n// #%s" % self.attr("id"))
        if self.has_transform() or self.hasClip():
            self.ctx.save()

    def createLinearGradient(self):
        x1, y1, x2, y2 = self.gradient.get_data()
        self.ctx.createLinearGradient("grad", x1, y1, x2, y2)
        for stop in self.gradient.stops:
            color = self.ctx.getColor(stop.split(";")[0].split(":")[1] , stop.split(";")[1].split(":")[1])
            offset = float(stop.split(";")[2].split(":")[1])
            self.ctx.addColorStop("grad", offset, color)
        

    def draw(self, isClip=False):
        data = self.get_data()
        if self.has_transform():
            trans_matrix = self.get_transform()
            self.ctx.transform(*trans_matrix) # unpacks argument list
        if not isClip:
            style = self.get_style()
            self.set_style(style)
            self.ctx.beginPath()
            
        # unpacks "data" in parameters to given method
        getattr(self.ctx, self.command)(*data)
          
        if not isClip:
            self.ctx.closePath()
    
    def drawClip(self):
        clipId = self.getClipId()
        elementClip = self.rootTree.getClipPath(clipId)
        self.ctx.beginPath()
        if (self.has_transform()):
            self.ctx.save()
            transMatrix = self.get_transform()
            self.ctx.transform(*transMatrix)
        #DRAW
        elementClip.runDraw(True)
        if (self.has_transform()):
            self.ctx.restore()
        self.ctx.clip()   

    def endDraw(self):
        if self.has_transform() or self.hasClip():
            self.ctx.restore()