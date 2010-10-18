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
    
    def __init__(self, context = "ctx"):
        self.obj = context
        self.code = ""  #stores the code
        self.styles = {}   #stores the last style applied
        self.code = "var canvas = document.getElementById('canvas');"
        self.code += "%s = canvas.getContext(\"2d\");" % self.obj
    
    def write(self, text):
        self.code += text + "\n"
    
    def output(self):
        """Writes the code to a file"""
        #temporary ouput for faster tests
        f = open("canvas.html", "w")
        f.write("<html><body>\n")
        f.write("<canvas id='canvas' width='800' height='600'></canvas>\n")
        f.write("<script>\n" + self.code)
        f.write("\n</script></body></html>")
        f.close()
    
    def equalStyle(self, st, key):
        """Checks if the last style used is the same or there's no style yet"""
        if not self.styles.has_key(key): return False
        if not st.has_key(key): return True
        return st[key] == self.styles[key]
    
    def beginPath(self, elem):
        self.write("\n//Element %s" % elem)
        self.write("%s.beginPath();" % self.obj)
    
    def closePath(self):
        self.write("%s.closePath();" % self.obj)
    
    def stroke(self, style):
        if style.has_key("stroke") and style["stroke"] != "none":
            self.write("%s.stroke();" % self.obj)
    
    def fill(self, style):
        if style.has_key("fill") and style["fill"] != "none":
            self.write("%s.fill();" % self.obj)
    
    def fillStyle(self, st):
        if not st.has_key("fill"): return
        if st["fill"] == "none": return
        if self.equalStyle(st, "fill"):
            if self.equalStyle(st, "fill-opacity"): return
        elif st.has_key("fill-opacity"):
            a = st["fill-opacity"]
        else:
            a = 1
        self.out("%s.fillStyle = %s;" % (self.obj, self.set_color(st["fill"], a)))
    
    def strokeStyle(self, st):
        if not st.has_key("stroke"): return
        if st["stroke"] == "none": return
        if self.equalStyle(st, "stroke"):
            if self.equalStyle(st, "stroke-opacity"): return
        elif st.has_key("stroke-opacity"):
            a = st["stroke-opacity"]
        else:
            a = 1
        self.out("%s.strokeStyle = %s;" % (self.obj, self.set_color(st["stroke"], a)))
    
    def globalAlpha(self, st):
        if not st.has_key("opacity"):
            if self.styles.has_key("opacity") and float(self.styles["opacity"] < 1):
                self.write("%s.globalAlpha = 1;" % self.obj)
            return
        if float(st["opacity"]) == 1 or self.equalStyle(st, "opacity"): return
        self.write("%s.globalAlpha = %.1f;" % (self.obj, float(st["opacity"])))
    
    def lineWidth(self, st):
        if not st.has_key("stroke-width"): return
        if self.equalStyle(st, "stroke-width"): return
        data = (self.obj, inkex.unittouu(st["stroke-width"]))
        self.write("%s.lineWidth = %.2f;" % (data))
    
    def lineCap(self, st):
        if not st.has_key("stroke-linecap"): return
        if self.equalStyle(st, "stroke-linecap"): return
        self.write("%s.lineCap = '%s';" % (self.obj, st["stroke-linecap"]))
    
    def lineJoin(self, st):
        if not st.has_key("stroke-linejoin"): return
        if self.equalStyle(st, "stroke-linejoin"): return
        self.write("%s.lineJoin = '%s';" % (self.obj, st["stroke-linejoin"]))

    def miterLimit(self, st):
        if not st.has_key("stroke-miterlimit"): return
        if self.equalStyle(st, "stroke-miterlimit"): return
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
        
    def translate(self, cx, cy):
        self.write("%s.translate(%.2f, %.2f);" % (self.obj, cx, cy))
    
    def rotate(self, angle):
        if angle == 0: return
        self.write("%s.rotate(%.2f);" % (self.obj, angle))
        
    def scale(self, rx, ry):
        if rx == ry == 1: return
        self.write("%s.scale(%.2f, %.2f);" % (self.obj, rx, ry))


class Ink2Canvas(inkex.Effect):
    def __init__(self, ctx):
        inkex.Effect.__init__(self)

    def set_gradient(self, href):
        g = self.xpathSingle("//*[@id='%s']" % href)
        if g.get("r"):
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
        gstops = self.xpathSingle("//svg:linearGradient[@id='%s']" % gstops[1:])
        for stop in gstops:
            style = parseStyle(stop.get("style"))
            stop_color = style["stop-color"]
            opacity = style["stop-opacity"]
            color = self.set_color(stop_color, opacity)
            pos = float(stop.get("offset"))
            c.addColorStop(href, pos, color)
        return href

    def set_color(self, rgb, a):
        """Returns rgba or hex, depending of alpha value"""
        #if references a gradient definition. Format: url(#linearGrad)
        if rgb[:3] == "url": return self.set_gradient(rgb[5:-1])
        if float(a) == 1.0: return "'%s'" % rgb
        
        #removes the '#'
        rgb = rgb[1:]
        r = int(rgb[:2], 16)
        g = int(rgb[2:4], 16)
        b = int(rgb[4:], 16)
        a = float(a)
        return "'rgba(%d, %d, %d, %.1f)'" % (r, g, b, a)

    def draw_rect(self, c, node):
        """Draws svg:rect elements"""
        x = float(node.get("x"))
        y = float(node.get("y"))
        w = float(node.get("width"))
        h = float(node.get("height"))
        rx = float(node.get("rx"))
        ry = float(node.get("ry"))
        c.rect(x, y, w, h, rx, ry)
    
    def draw_path(self, c, node):
        """Draws svg:path elements"""
        #stores the current "pen" position
        curr = []

        path = parsePath(node.get("d"))
        for pt in path:
            cmm = pt[0]
            data = pt[1]
            if cmm == "M":
                c.moveTo(data[0], data[1])

            elif cmm == "L":
                c.lineTo(data[0], data[1])

            elif cmm == "C":
                curr = data[4], data[5]
                x1, y1, x2, y2 = data[0], data[1], data[2], data[3]
                x, y = data[4], data[5]
                c.bezierCurveTo(x1, y1, x2, y2, x, y)

            elif cmm == "A":
                #http://www.w3.org/TR/SVG11/implnote.html#ArcImplementationNotes
                # code adapted from http://code.google.com/p/canvg/
                import math
                x1 = curr[0]
                y1 = curr[1]
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

                c.translate(cx, cy)
                c.rotate(angle)
                c.scale(sx, sy)
                c.arc(0, 0, r, a1, a1 + ad, 1 - sweepflag)
                c.scale(1/sx, 1/sy)
                c.rotate(-angle)
                c.translate(-cx, -cy)
                curr = x2, y2

    def effect(self):
        """Applies the effect"""

        c = Canvas()
        for nid, node in self.selected.iteritems():
            c.beginPath(node.get("id"))

            #parse the element style properties into a dictionary
            style = parseStyle(node.get("style"))
            c.globalAlpha(style)
            c.lineWidth(style)
            c.lineCap(style)
            c.lineJoin(style)
            c.miterLimit(style)
            c.strokeStyle(style)
            c.fillStyle(style)

            #get the node type and call the appropriate method
            if node.tag == inkex.addNS("path", "svg"):
                self.draw_path(c, node)
            elif node.tag == inkex.addNS("rect", "svg"):
                self.draw_rect(c, node)
            elif node.tag == inkex.addNS("text", "svg"):
                pass
            elif node.tag == inkex.addNS("g", "svg"):
                pass

            c.fill(style)
            c.stroke(style)
            #saves style to compare in next iteration
            c.styles = style
            c.closePath()

        self.output()
        
ink = Ink2Canvas()
ink.affect()
