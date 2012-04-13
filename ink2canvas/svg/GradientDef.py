from ink2canvas.svg.Element import Element

class GradientDef(Element):
    def __init__(self, node, stops):
        self.node = node
        self.stops = stops