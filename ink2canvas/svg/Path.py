from ink2canvas.svg.AbstractShape import AbstractShape
from ink2canvas.lib.simplepath import parsePath

class Path(AbstractShape):
    def getData(self):
        #path data is already converted to float
        return parsePath(self.attr("d"))

    def pathMoveTo(self, data):
        self.canvasContext.moveTo(data[0], data[1])
        self.currentPosition = data[0], data[1]

    def pathLineTo(self, data):
        self.canvasContext.lineTo(data[0], data[1])
        self.currentPosition = data[0], data[1]

    def pathCurveTo(self, data):
        x1, y1, x2, y2 = data[0], data[1], data[2], data[3]
        x, y = data[4], data[5]
        self.canvasContext.bezierCurveTo(x1, y1, x2, y2, x, y)
        self.currentPosition = x, y

    def pathArcTo(self, data):
        #http://www.w3.org/TR/SVG11/implnote.html#ArcImplementationNotes
        # code adapted from http://code.google.com/p/canvg/
        import math
        x1 = self.currentPosition[0]
        y1 = self.currentPosition[1]
        x2 = data[5]
        y2 = data[6]
        rx = data[0]
        ry = data[1]
        angle = data[2] * (math.pi / 180.0)
        arcFlag = data[3]
        sweepFlag = data[4]

        if x1 == x2 and y1 == y2:
            return

        #compute (x1', y1')
        _x1 = math.cos(angle) * (x1 - x2) / 2.0 + math.sin(angle) * (y1 - y2) / 2.0
        _y1 = -math.sin(angle) * (x1 - x2) / 2.0 + math.cos(angle) * (y1 - y2) / 2.0

        #adjust radii
        l = _x1**2 / rx**2 + _y1**2 / ry**2
        if l > 1:
            rx *= math.sqrt(l)
            ry *= math.sqrt(l)

        #compute (cx', cy')
        numr = (rx**2 * ry**2) - (rx**2 * _y1**2) - (ry**2 * _x1**2)
        demr = (rx**2 * _y1**2) + (ry**2 * _x1**2)
        sig = -1 if arcFlag == sweepFlag else 1
        sig = sig * math.sqrt(numr / demr)
        if math.isnan(sig): sig = 0;
        _cx = sig * rx * _y1 / ry
        _cy = sig * -ry * _x1 / rx

        #compute (cx, cy) from (cx', cy')
        cx = (x1 + x2) / 2.0 + math.cos(angle) * _cx - math.sin(angle) * _cy
        cy = (y1 + y2) / 2.0 + math.sin(angle) * _cx + math.cos(angle) * _cy

        #compute startAngle & endAngle
        #vector magnitude
        m = lambda v: math.sqrt(v[0]**2 + v[1]**2)
        #ratio between two vectors
        r = lambda u, v: (u[0] * v[0] + u[1] * v[1]) / (m(u) * m(v))
        #angle between two vectors
        a = lambda u, v: (-1 if u[0]*v[1] < u[1]*v[0] else 1) * math.acos(r(u,v))
        #initial angle
        a1 = a([1,0], [(_x1 - _cx) / rx, (_y1 - _cy)/ry])
        #angle delta
        u = [(_x1 - _cx) / rx, (_y1 - _cy) / ry]
        v = [(-_x1 - _cx) / rx, (-_y1 - _cy) / ry]
        ad = a(u, v)
        if r(u,v) <= -1: ad = math.pi
        if r(u,v) >= 1: ad = 0

        if sweepFlag == 0 and ad > 0: ad = ad - 2 * math.pi;
        if sweepFlag == 1 and ad < 0: ad = ad + 2 * math.pi;

        r = rx if rx > ry else ry
        sx = 1 if rx > ry else rx / ry
        sy = ry / rx if rx > ry else 1

        self.canvasContext.translate(cx, cy)
        self.canvasContext.rotate(angle)
        self.canvasContext.scale(sx, sy)
        self.canvasContext.arc(0, 0, r, a1, a1 + ad, 1 - sweepFlag)
        self.canvasContext.scale(1/sx, 1/sy)
        self.canvasContext.rotate(-angle)
        self.canvasContext.translate(-cx, -cy)
        self.currentPosition = x2, y2

    def draw(self, isClip=False):
        path = self.getData()
        if not isClip:
            style = self.getStyle()
            self.setStyle(style)
            self.canvasContext.beginPath()
        if self.hasTransform():
            transMatrix = self.getTransform()
            self.canvasContext.transform(*transMatrix) # unpacks argument list

        #Draws path commands
        pathCommand = {"M": self.pathMoveTo,
                       "L": self.pathLineTo,
                       "C": self.pathCurveTo,
                       "A": self.pathArcTo}
        for pt in path:
            comm, data = pt
            if comm in pathCommand:
                pathCommand[comm](data)

        gradientFill = self.gradientHelper.setGradientFill()
        gradientStroke = self.gradientHelper.setGradientStroke()
        
        if not isClip: 
            self.canvasContext.closePath(comm == "Z")
            if(not gradientFill):        
                self.canvasContext.fill()
            if(not gradientStroke):
                self.canvasContext.stroke()