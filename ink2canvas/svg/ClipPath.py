from ink2canvas.svg import Element

class Clippath(Element):

    def __init__(self, command, node, canvasContext, root):
        Element.__init__(self)
        self.node = node