#!/usr/bin/env python
'''
Copyright (C) 2010 Karlisson Bezerra, contato@nerdson.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

import inkex
import simplestyle 
from simplepath import parsePath
from simpletransform import parseTransform

log = inkex.debug  #alias to debug method


class Canvas:
    """Canvas API helper class"""

    def __init__(self, svg, width, height, context = "ctx"):
        self.obj = context
        self.code = []  #stores the code
        self.svg = svg  #for xpath expression searchs
        self.style = {}
        self.styleCache = {}  #stores the previous style applied
        self.width = width
        self.height = height

    def write(self, text):
        self.code.append("\t" + text + "\n")

    def output(self):
        from textwrap import dedent
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Inkscape Output</title>
        </head>
        <body>
            <canvas id='canvas' width='%d' height='%d'></canvas>
            <script>
            var %s = document.getElementById("canvas").getContext("2d");
            %s
            </script>
        </body>
        </html>
        """
        return dedent(html) % (self.width, self.height, self.obj, "".join(self.code))

    def equalStyle(self, style, key):
        """Checks if the last style used is the same or there's no style yet"""
        if key in self.styleCache:
            return True
        if key not in style:
            return True
        return style[key] == self.styleCache[key]

    def beginPath(self, elem):
        self.write("\n//Element %s" % elem)
        self.write("%s.beginPath();" % self.obj)

    def createLinearGradient(self, href, x1, y1, x2, y2):
        data = (href, self.obj, x1, y1, x2, y2)
        self.write("var %s = %s.createLinearGradient(%.2f,%.2f,%.2f,%.2f);" % data)

    def createRadialGradient(self, href, cx1, cy1, rx, cx2, cy2, ry):
        data = (href, self.obj, cx1, cy1, rx, cx2, cy2, ry)
        self.write("var %s = %s.createRadialGradient(%.2f,%.2f,%.2f,%.2f,%.2f,%.2f);" % data)

    def addColorStop(self, href, pos, color):
        self.write("%s.addColorStop(%.2f, %s);" % (href, pos, color))

    def getColor(self, rgb, a):
        r, g, b = simplestyle.parseColor(rgb)
        a = float(a)
        if a < 1:
            return "'rgba(%d, %d, %d, %.1f)'" % (r, g, b, a)
        else:
            return "'rgb(%d, %d, %d)'" % (r, g, b)

    def setGradient(self, href):
        try:
            g = self.svg.xpath("//*[@id='%s']" % href, namespaces=inkex.NSS)[0]
        except:
            return
        
        if g.get("r"):
            cx = float(g.get("cx"))
            cy = float(g.get("cy"))
            r = float(g.get("r"))
            self.createRadialGradient(href, cx, cy, r, cx, cy, r)
        else:
            x1 = float(g.get("x1"))
            y1 = float(g.get("y1"))
            x2 = float(g.get("x2"))
            y2 = float(g.get("y2"))
            self.createLinearGradient(href, x1, y1, x2, y2)

        #get gradient color stops
        gstops = g.get(inkex.addNS("href", "xlink"))
        gstops = self.svg.xpath("//svg:linearGradient[@id='%s']" % gstops[1:], namespaces=inkex.NSS)[0]
        for stop in gstops:
            style = simplestyle.parseStyle(stop.get("style"))
            stop_color = style["stop-color"]
            opacity = style["stop-opacity"]
            color = self.getColor(stop_color, opacity)
            pos = float(stop.get("offset"))
            self.addColorStop(href, pos, color)
        return href

    def fillHelper(self, rgb, alpha):
        """Returns rgba or hex, depending on alpha value"""
        #if references a gradient definition. Format: url(#linearGrad)
        if "url(" in rgb:
            return self.setGradient(rgb[5:-1])
        return self.getColor(rgb, alpha)

    def setOpacity(self, value):
        self.write("%s.globalAlpha = %.1f;" % (self.obj, float(value)))

    def setFill(self, value):
        if "fill-opacity" in self.style:
            alpha = self.style["fill-opacity"]
        else:
            alpha = 1
        fill = self.fillHelper(value, alpha)
        if fill:
            self.write("%s.fillStyle = %s;" % (self.obj, fill))

    def setStroke(self, value):
        if "stroke-opacity" in self.style:
            alpha = self.style["stroke-opacity"]
        else:
            alpha = 1
        self.write("%s.strokeStyle = %s;" % (self.obj, self.fillHelper(value, alpha)))

    def setStrokeWidth(self, value):
        self.write("%s.lineWidth = %.2f;" % (self.obj, inkex.unittouu(value)))

    def setStrokeLinecap(self, value):
        self.write("%s.lineCap = '%s';" % (self.obj, value))

    def setStrokeLinejoin(self, value):
        self.write("%s.lineJoin = '%s';" % (self.obj, value))

    def setStrokeMiterlimit(self, value):
        self.write("%s.miterLimit = %s;" % (self.obj, value))

    def moveTo(self, x, y):
        self.write("%s.moveTo(%.2f, %.2f);" % (self.obj, x, y))

    def lineTo(self, x, y):
        self.write("%s.lineTo(%.2f, %.2f);" % (self.obj, x, y))

    def quadraticCurveTo(self, cpx, cpy, x, y):
        data = (self.obj, cpx, cpy, x, y)
        self.write("%s.quadraticCurveTo(%.2f, %.2f, %.2f, %.2f);" % data)

    def bezierCurveTo(self, x1, y1, x2, y2, x, y):
        data = (self.obj, x1, y1, x2, y2, x, y)
        self.write("%s.bezierCurveTo(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f);" % data)

    def rect(self, x, y, w, h, rx = 0, ry = 0):
        if rx or ry:
            #rounded rectangle, starts top-left anticlockwise
            self.moveTo(x, y + ry)
            self.lineTo(x, y+h-ry)
            self.quadraticCurveTo(x, y+h, x+rx, y+h)
            self.lineTo(x+w-rx, y+h)
            self.quadraticCurveTo(x+w, y+h, x+w, y+h-ry)
            self.lineTo(x+w, y+ry)
            self.quadraticCurveTo(x+w, y, x+w-rx, y)
            self.lineTo(x+rx, y)
            self.quadraticCurveTo(x, y, x, y+ry)
        else:
            self.write("%s.rect(%.2f, %.2f, %.2f, %.2f);" % (self.obj, x, y, w, h))

    def arc(self, x, y, r, a1, a2, flag):
        data = (self.obj, x, y, r, a1, a2, flag)
        self.write("%s.arc(%.2f, %.2f, %.2f, %.2f, %.2f, %d);" % data)

    def fillText(self, text, x, y):
        self.write("%s.fillText(\"%s\", %.2f, %.2f);" % (self.obj, text, x, y))

    def translate(self, cx, cy):
        self.write("%s.translate(%.2f, %.2f);" % (self.obj, cx, cy))

    def rotate(self, angle):
        self.write("%s.rotate(%.2f);" % (self.obj, angle))

    def scale(self, rx, ry):
        self.write("%s.scale(%.2f, %.2f);" % (self.obj, rx, ry))

    def transform(self, m11, m12, m21, m22, dx, dy):
        self.write("%s.transform(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f);" \
                    % (self.obj, m11, m12, m21, m22, dx, dy))

    def save(self):
        self.write("%s.save();" % self.obj)

    def restore(self):
        self.write("%s.restore();" % self.obj)

    def closePath(self):
        if "fill" in self.style and self.style["fill"] != "none":
            self.write("%s.fill();" % self.obj)
        if "stroke" in self.style and self.style["stroke"] != "none":
            self.write("%s.stroke();" % self.obj)
        #self.write("%s.closePath();" % self.obj)


class Ink2Canvas(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.currentPosition = []  #stores the current "pen" position
        self.content = ""

    def setStyle(self, ctx, node):
        """Translates style properties names into method calls"""
        style = simplestyle.parseStyle(node.get("style"))
        #remove any trailing space in dict keys/values
        style = dict([(str.strip(k), str.strip(v)) for k,v in style.items()])
        ctx.style = style
        for key in style:
            tmp_list = map(str.capitalize, key.split("-"))
            method = "set" + "".join(tmp_list)
            if hasattr(ctx, method) and style[key] != "none":
                getattr(ctx, method)(style[key])
        #saves style to compare in next iteration
        ctx.styleCache = style

    def setTransform(self, ctx, node):
        data = node.get("transform")
        if not data:
            return
        matrix = parseTransform(data)
        m11, m21, dx = matrix[0]
        m12, m22, dy = matrix[1]
        print matrix
        ctx.transform(m11, m12, m21, m22, dx, dy)

    def drawAbstractShape(self, ctx, node, callback, args):
        """Gets the node type and calls the given method"""
        ctx.beginPath(node.get("id"))
        self.setStyle(ctx, node)
        ctx.save()
        self.setTransform(ctx, node)
        callback(*args) # unpacks "args" in parameters to method passed
        ctx.closePath()
        ctx.restore()

    def drawRect(self, ctx, node):
        x = float(node.get("x"))
        y = float(node.get("y"))
        w = float(node.get("width"))
        h = float(node.get("height"))
        rx = node.get("rx")
        ry = node.get("ry")
        rx = float(rx) if rx else 0
        ry = float(ry) if ry else 0
        args = [x, y, w, h, rx, ry]
        self.drawAbstractShape(ctx, node, ctx.rect, args)

    def drawCircle(self, ctx, node):
        import math
        cx = float(node.get("cx"))
        cy = float(node.get("cy"))
        r = float(node.get("r"))
        args = [cx, cy, r, 0, math.pi * 2, True]
        self.drawAbstractShape(ctx, node, ctx.arc, args)

    def ellipseHelper(self, ctx, cx, cy, rx, ry):
        import math
        KAPPA = 4 * ((math.sqrt(2) - 1) / 3)
        ctx.moveTo(cx, cy - ry)
        ctx.bezierCurveTo(cx + (KAPPA * rx), cy - ry,  cx + rx, cy - (KAPPA * ry), cx + rx, cy)
        ctx.bezierCurveTo(cx + rx, cy + (KAPPA * ry), cx + (KAPPA * rx), cy + ry, cx, cy + ry)
        ctx.bezierCurveTo(cx - (KAPPA * rx), cy + ry, cx - rx, cy + (KAPPA * ry), cx - rx, cy)
        ctx.bezierCurveTo(cx - rx, cy - (KAPPA * ry), cx - (KAPPA * rx), cy - ry, cx, cy - ry)

    def drawEllipse(self, ctx, node):
        cx = float(node.get("cx"))
        cy = float(node.get("cy"))
        rx = float(node.get("rx"))
        ry = float(node.get("ry"))
        args = [ctx, cx, cy, rx, ry]
        self.drawAbstractShape(ctx, node, self.ellipseHelper, args)

    def pathMoveTo(self, ctx, data):
        ctx.moveTo(data[0], data[1])
        self.currentPosition = data[0], data[1]

    def pathLineTo(self, ctx, data):
        ctx.lineTo(data[0], data[1])
        self.currentPosition = data[0], data[1]

    def pathCurveTo(self, ctx, data):
        x1, y1, x2, y2 = data[0], data[1], data[2], data[3]
        x, y = data[4], data[5]
        ctx.bezierCurveTo(x1, y1, x2, y2, x, y)
        self.currentPosition = x, y

    def pathArcTo(self, ctx, data):
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
        arcflag = data[3]
        sweepflag = data[4]

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
        sig = -1 if arcflag == sweepflag else 1
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

        if sweepflag == 0 and ad > 0: ad = ad - 2 * math.pi;
        if sweepflag == 1 and ad < 0: ad = ad + 2 * math.pi;

        r = rx if rx > ry else ry
        sx = 1 if rx > ry else rx / ry
        sy = ry / rx if rx > ry else 1

        ctx.translate(cx, cy)
        ctx.rotate(angle)
        ctx.scale(sx, sy)
        ctx.arc(0, 0, r, a1, a1 + ad, 1 - sweepflag)
        ctx.scale(1/sx, 1/sy)
        ctx.rotate(-angle)
        ctx.translate(-cx, -cy)
        self.currentPosition = x2, y2

    def drawPathHelper(self, ctx, path):
        """Draws path commands"""
        pathCommand = {"M": self.pathMoveTo,
                       "L": self.pathLineTo,
                       "C": self.pathCurveTo,
                       "A": self.pathArcTo}
        for pt in path:
            comm, data = pt
            if comm in pathCommand:
                pathCommand[comm](ctx, data)

    def drawPath(self, ctx, node):
        #path data is already converted to float
        path = parsePath(node.get("d"))
        #need to call another method to draw path commands
        self.drawAbstractShape(ctx, node, self.drawPathHelper, [ctx, path])

    def drawLine(self, ctx, node):
        x1 = float(node.get("x1"))
        y1 = float(node.get("y1"))
        x2 = float(node.get("x2"))
        y2 = float(node.get("y2"))
        path = [["M", [x1, y1]], ["L", [x2, y2]]]
        self.drawAbstractShape(ctx, node, self.drawPathHelper, [ctx, path])
 
    def drawPolygon(self, ctx, node):
        points = node.get("points").strip().split(" ")
        points = map(lambda x: x.split(","), points)
        comm = []
        for pt in points:           #creating path command similar
            pt = map(float, pt)
            comm.append(["L", pt])
        comm[0][0] = "M"            #first command must be a 'M' => moveTo
        self.drawAbstractShape(ctx, node, self.drawPathHelper, [ctx, comm])
 
    def drawPolyline(self, ctx, node):
        self.drawPolygon(ctx, node)

    def drawText(self, ctx, node):
        self.setStyle(ctx, node)
        x = float(node.get("x"))
        y = float(node.get("y"))
        ctx.fillText("Teste", x, y)

    def drawG(self, ctx, node):
        """Recursive method to iterate through SVG groups"""
        #get layer label, if exists
        group = node.get(inkex.addNS("groupmode", "inkscape"))
        if group == "layer":
            ctx.write("\n//" + node.get(inkex.addNS("label", "inkscape")))
        
        for child in node:
            #remove namespace part from {http://www.w3.org/2000/svg}path
            tagtype = child.tag.split("}")[1]
            method = "draw" + tagtype.capitalize()  #"draw" + "Path"
            if hasattr(self, method):
                getattr(self, method)(ctx, child)

    def output(self):
        import sys
        sys.stdout.write(self.content)

    def effect(self):
        """Applies the effect"""
        svg = self.document.getroot()
        width = inkex.unittouu(svg.get("width"))
        height = inkex.unittouu(svg.get("height"))
        ctx = Canvas(self.document, width, height)
        #starts parsing groups passing root element
        self.drawG(ctx, svg)
        self.content = ctx.output()

if __name__ == "__main__":
    ink = Ink2Canvas()
    ink.affect()
