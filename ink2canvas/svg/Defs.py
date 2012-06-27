from ink2canvas.svg.Element import Element

class Defs(Element):
    def __init__(self, command, node, canvasContext, root):
        Element.__init__(self)
        self.command = command
        self.node = node
        self.canvasContext = canvasContext
        self.root = root