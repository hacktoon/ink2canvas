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
from simplestyle import parseStyle
from simplepath import parsePath

log = inkex.debug  #alias to debug method


class Canvas:
    """Canvas API helper class"""
    
    def __init__(self, width, height, context = "ctx"):
        self.obj = context
        self.code = []  #stores the code
        self.styleCache = {}  #stores the previous style applied
        self.width = width
        self.height = height
    
    def write(self, text):
        self.code.append("\t" + text + "\n")
    
    def output(self):
        #temporary ouput for faster tests
        f = open("canvas.html", "w")
        f.write("<html><body>\n")
        f.write("<canvas id='canvas' width='%.2f' height='%.2f'>" % (self.width, self.height))
        f.write("</canvas>\n<script>\n")
        f.write('var %s = document.getElementById("canvas").getContext("2d");' % self.obj)
        f.writelines(self.code)
        f.write("\n</script></body></html>")
        f.close()

    def equalStyle(self, style, key):
        """Checks if the last style used is the same or there's no style yet"""
        if not self.styleCache.has_key(key):
            return False
        if not style.has_key(key):
            return True
        return style[key] == self.styleCache[key]
    
    def beginPath(self, elem):
        self.write("\n//Element %s" % elem)
        self.write("%s.beginPath();" % self.obj)
    
    def closePath(self):
        self.write("%s.closePath();" % self.obj)
        
    def set_gradient(self, href):
        g = inkex.xpathSingle("//*[@id='%s']" % href)
        if g and g.get("r"):
            cx = float(g.get("cx"))
            cy = float(g.get("cy"))
            r = float(g.get("r"))
            c.createRadialGradient(href, cx, cy, r, cx, cy, r)
        else:
            x1 = float(g.get("x1"))
            y1 = float(g.get("y1"))
            x2 = float(g.get("x2"))
            y2 = float(g.get("y2"))
            c.createLinearGradient(href, x1, y1, x2, y2)
        
        #get the gradient stops
        gstops = g.get(inkex.addNS("href", "xlink"))
        gstops = inkex.xpathSingle("//svg:linearGradient[@id='%s']" % gstops[1:])
        for stop in gstops:
            style = parseStyle(stop.get("style"))
            stop_color = style["stop-color"]
            opacity = style["stop-opacity"]
            color = self.set_color(stop_color, opacity)
            pos = float(stop.get("offset"))
            c.addColorStop(href, pos, color)
        return href

    def set_color(self, rgb, a):
        """Returns rgba or hex, depending on alpha value"""
        #if references a gradient definition. Format: url(#linearGrad)
        if rgb[:3] == "url":
            return self.set_gradient(rgb[5:-1])
        if float(a) == 1.0:
            return "'%s'" % rgb

        #removes the '#'
        rgb = rgb[1:]
        r = int(rgb[:2], 16)
        g = int(rgb[2:4], 16)
        b = int(rgb[4:], 16)
        a = float(a)
        return "'rgba(%d, %d, %d, %.1f)'" % (r, g, b, a)

    def stroke(self, style):
        if style.has_key("stroke") and style["stroke"] != "none":
            self.write("%s.stroke();" % self.obj)
    
    def fill(self, style):
        if style.has_key("fill") and style["fill"] != "none":
            self.write("%s.fill();" % self.obj)
    
    def fillStyle(self, style):
        if not style.has_key("fill"):
            return
        if style["fill"] == "none":
            return
        if self.equalStyle(style, "fill"):
            if self.equalStyle(style, "fill-opacity"):
                return
        elif style.has_key("fill-opacity"):
            a = style["fill-opacity"]
        else:
            a = 1
        self.write("%s.fillStyle = %s;" % (self.obj, self.set_color(style["fill"], a)))
    
    def strokeStyle(self, style):
        if not style.has_key("stroke"):
            return
        if style["stroke"] == "none":
            return
        if self.equalStyle(style, "stroke"):
            if self.equalStyle(style, "stroke-opacity"):
                return
        elif style.has_key("stroke-opacity"):
            a = style["stroke-opacity"]
        else:
            a = 1
        self.write("%s.strokeStyle = %s;" % (self.obj, self.set_color(style["stroke"], a)))
    
    def globalAlpha(self, style):
        if not style.has_key("opacity"):
            if self.styleCache.has_key("opacity") and float(self.styleCache["opacity"] < 1):
                self.write("%s.globalAlpha = 1;" % self.obj)
            return
        if float(style["opacity"]) == 1 or self.equalStyle(style, "opacity"):
            return
        self.write("%s.globalAlpha = %.1f;" % (self.obj, float(style["opacity"])))
    
    def lineWidth(self, style):
        if not style.has_key("stroke-width"):
            return
        if self.equalStyle(style, "stroke-width"):
            return
        data = (self.obj, inkex.unittouu(style["stroke-width"]))
        self.write("%s.lineWidth = %.2f;" % (data))
    
    def lineCap(self, style):
        if not style.has_key("stroke-linecap"):
            return
        if self.equalStyle(style, "stroke-linecap"):
            return
        self.write("%s.lineCap = '%s';" % (self.obj, style["stroke-linecap"]))
    
    def lineJoin(self, style):
        if not style.has_key("stroke-linejoin"):
            return
        if self.equalStyle(style, "stroke-linejoin"):
            return
        self.write("%s.lineJoin = '%s';" % (self.obj, style["stroke-linejoin"]))

    def miterLimit(self, style):
        if not style.has_key("stroke-miterlimit"):
            return
        if self.equalStyle(style, "stroke-miterlimit"):
            return
        self.write("%s.miterLimit = %s;" % (self.obj, style["stroke-miterlimit"]))
    
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

    def createLinearGradient(self, href, x1, y1, x2, y2):
        data = (self.obj, href, x1, y1, x2, y2)
        self.write("var %s = %s.createLinearGradient(%.2f,%.2f,%.2f,%.2f);" % data)

    def createRadialGradient(self, href, cx1, cy1, rx, cx2, cy2, ry):
        data = (self.obj, href, cx1, cy1, rx, cx2, cy2, ry)
        self.write("var %s = %s.createRadialGradient(%.2f,%.2f,%.2f,%.2f,%.2f,%.2f);" % data)

    def addColorStop(self, href, pos, color):
        self.write("%s.addColorStop(%.2f, %s);" % (href, pos, color))
        
    def fillText(self, text, x, y):
        self.write("%s.fillText(\"%s\", %.2f, %.2f);" % (self.obj, text, x, y))

    def translate(self, cx, cy):
        self.write("%s.translate(%.2f, %.2f);" % (self.obj, cx, cy))

    def rotate(self, angle):
        self.write("%s.rotate(%.2f);" % (self.obj, angle))

    def scale(self, rx, ry):
        if rx == ry == 1:
            return
        self.write("%s.scale(%.2f, %.2f);" % (self.obj, rx, ry))


class Ink2Canvas(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.drawMethod = {}
        #stores the current "pen" position
        self.currentPosition = []

    def setStyle(self, ctx, style):
        #parse the element style properties into a dictionary
        ctx.globalAlpha(style)
        ctx.lineWidth(style)
        ctx.lineCap(style)
        ctx.lineJoin(style)
        ctx.miterLimit(style)
        ctx.strokeStyle(style)
        ctx.fillStyle(style)
    
    def setTextStyle(self, ctx, style):
        pass

    def drawAbstractShape(self, ctx, node, callback, args):
        """Gets the node type and call the given method"""
        style = parseStyle(node.get("style"))
        
        ctx.beginPath(node.get("id"))
        self.setStyle(ctx, style)
        #calling the appropriate method, expands "args" in parameters to callback
        callback(*args)
        ctx.fill(style)
        ctx.stroke(style)
        #saves style to compare in next iteration
        ctx.prev_style = style
        ctx.closePath()

    def drawRect(self, ctx, node):
        """Draws svg:rect elements"""
        x = float(node.get("x"))
        y = float(node.get("y"))
        w = float(node.get("width"))
        h = float(node.get("height"))
        rx = float(node.get("rx"))
        ry = float(node.get("ry"))
        args = [x, y, w, h, rx, ry]
        self.drawAbstractShape(ctx, node, ctx.rect, args)

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
        pathCommand = {"M": self.pathMoveTo,
                       "L": self.pathLineTo,
                       "C": self.pathCurveTo,
                       "A": self.pathArcTo}
        for pt in path:
            cmm = pt[0]
            data = pt[1]
            if pathCommand.has_key(cmm):
                pathCommand[cmm](ctx, data)
    
    def drawPath(self, ctx, node):
        """Draws svg:path elements"""
        #path data is already converted to float
        path = parsePath(node.get("d"))
        args = [ctx, path]
        self.drawAbstractShape(ctx, node, self.drawPathHelper, args)

    def drawText(self, ctx, node):
        style = parseStyle(node.get("style"))
        self.setTextStyle(ctx, style)
        x = float(node.get("x"))
        y = float(node.get("y"))
        ctx.fillText("Teste", x, y)

    def iterate(self, ctx, node):
        """Recursive method to iterate through elements"""
        #get layer label, if exists
        group = node.get(inkex.addNS("groupmode", "inkscape"))
        if group == "layer":
            ctx.write("\n//" + node.get(inkex.addNS("label", "inkscape")))
        
        for child in node:
            if self.drawMethod.has_key(child.tag):
                self.drawMethod[child.tag](ctx, child)

    def effect(self):
        """Applies the effect"""
       
        #define callbacks for drawing methods
        self.drawMethod[inkex.addNS("path", "svg")] = self.drawPath
        self.drawMethod[inkex.addNS("rect", "svg")] = self.drawRect
        self.drawMethod[inkex.addNS("text", "svg")] = self.drawText
        self.drawMethod[inkex.addNS("g", "svg")] = self.iterate
        
        svg = self.document.getroot()
        width = inkex.unittouu(svg.get("width"))
        height = inkex.unittouu(svg.get("height"))
        
        ctx = Canvas(width, height)
        self.iterate(ctx, svg)

        ctx.output()

ink = Ink2Canvas()
ink.affect()
