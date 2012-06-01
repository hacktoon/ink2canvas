from ink2canvas.svg.Element import Element

class Defs(Element):
    def __init__(self, command, node, ctx, root):
        Element.__init__(self)
        self.command = command
        self.node = node
        self.ctx = ctx
        self.root = root