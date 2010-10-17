#!/usr/bin/env python
'''
Copyright (C) 2009 Karlisson Bezerra, contato@nerdson.com

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

#overwrite debug method
log = inkex.debug


class Canvas(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.code = ""
        self.styles = {}

    def out(self, text):
        """Stores text to be written to a file later"""
        self.code += text + "\n"

    def set_color(self, rgb, a):
        """Returns rgba or hex, depending of alpha value"""
        if float(a) == 1.0:
            return "'%s';" % rgb
        rgb = rgb[1:]  # removes the '#'
        r = int(rgb[:2], 16)
        g = int(rgb[2:4], 16)
        b = int(rgb[4:], 16)
        a = float(a)
        return "'rgba(%d, %d, %d, %.1f)';" % (r, g, b, a)

    def set_style(self, style):
        """Sets the style methods"""
        if style.has_key("opacity") and float(style["opacity"]) < 1:
            self.out("ctx.globalAlpha = %.1f;" % float(style["opacity"]))

        #stroke properties
        if style.has_key("stroke-width"):
            self.out("ctx.lineWidth = %d;" % inkex.unittouu(style["stroke-width"]))

        if style.has_key("stroke-linecap"):
            self.out("ctx.lineCap = '%s';" % style["stroke-linecap"])

        if style.has_key("stroke-linejoin"):
            self.out("ctx.lineJoin = '%s';" % style["stroke-linejoin"])

        if style.has_key("stroke-miterlimit"):
            self.out("ctx.miterLimit = %s;" % style["stroke-miterlimit"])

        # stroke color
        if style.has_key("stroke") and style["stroke"] != "none":
            alpha = 1
            if style.has_key("stroke-opacity"):
                alpha = style["stroke-opacity"]
            self.out("ctx.strokeStyle = " + self.set_color(style["stroke"], alpha))

        # fill color
        if style.has_key("fill") and style["fill"] != "none":
            alpha = 1
            if style.has_key("fill-opacity"):
                alpha = style["fill-opacity"]
            self.out("ctx.fillStyle = " + self.set_color(style["fill"], alpha))

    def draw_rect(self, node):
        """Draws svg:rect elements"""
        #TODO: Add rounded rectangle support -  rx  ry
        x = float(node.get("x"))
        y = float(node.get("y"))
        w = float(node.get("width"))
        h = float(node.get("height"))
        self.out("ctx.rect(%.2f, %.2f, %.2f, %.2f);" % (x, y, w, h))
    
    def draw_path(self, node):
        """Draws svg:path elements"""
        #stores the current "pen" position
        curr = []

        path = parsePath(node.get("d"))
        for pt in path:
            cmm = pt[0]
            data = pt[1]
            if cmm == "M":
                curr = data[0], data[1]
                self.out("ctx.moveTo(%.2f, %.2f);" % curr)

            elif cmm == "L":
                curr = data[0], data[1]
                self.out("ctx.lineTo(%.2f, %.2f);" % curr)

            elif cmm == "C":
                curr = data[4], data[5]
                x1, y1, x2, y2 = data[0], data[1], data[2], data[3]
                x, y = data[4], data[5]
                bzr = "ctx.bezierCurveTo(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f);"
                self.out(bzr % (x1, y1, x2, y2, x, y))

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

                self.out("ctx.translate(%.2f, %.2f);" % (cx, cy))
                if angle != 0:
                    self.out("ctx.rotate(%.2f);" % angle)
                if sx != 1 or sy != 1:
                    self.out("ctx.scale(%.2f, %.2f);" % (sx, sy))
                self.out("ctx.arc(0, 0, %.2f, %.2f, %.2f, %d);" % (r, a1, a1 + ad, 1 - sweepflag))
                if sx != 1 or sy != 1:
                    self.out("ctx.scale(%.2f, %.2f);" % (1/sx, 1/sy))
                if angle != 0:
                    self.out("ctx.rotate(%.2f);" % -angle)
                self.out("ctx.translate(%.2f, %.2f);" % (-cx, -cy))

                curr = x2, y2

    def effect(self):
        """Applies the effect"""

        self.out("var draw = function(ctx) {")
        self.out("ctx = canvas.getContext(\"2d\");")

        for nid, node in self.selected.iteritems():
            
            self.out("\n// " + node.get("id"))
            self.out("ctx.beginPath();\n")

            #parse the element style properties into a dictionary
            style = parseStyle(node.get("style"))
            self.set_style(style)

            #get the node type and call the appropriate method
            if node.tag == inkex.addNS("path", "svg"):
                self.draw_path(node)
            elif node.tag == inkex.addNS("rect", "svg"):
                self.draw_rect(node)
            elif node.tag == inkex.addNS("text", "svg"):
                pass

            if style.has_key("fill") and style["fill"] != "none":
                self.out("\nctx.fill();")

            #finish the path
            if style.has_key("stroke") and style["stroke"] != "none":
                self.out("\nctx.stroke();")

            self.out("\nctx.closePath();")

            #reseting globalAlpha value
            if style.has_key("opacity") and float(style["opacity"]) < 1:
                self.out("ctx.globalAlpha = 1;")
        
        self.out("\n};")

        f = open("canvas.js", "w")
        f.write(self.code)
        f.close()

b = Canvas()
b.affect()
