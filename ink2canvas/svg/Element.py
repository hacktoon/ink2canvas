from ink2canvas.lib import inkex

class Element:
    def attr(self, val, ns=""):
        if ns:
            val = inkex.addNS(val, ns)
        try:
            attr = float(self.node.get(val))
        except:
            attr = self.node.get(val)
        return attr