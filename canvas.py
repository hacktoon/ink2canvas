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
        x = float(node.get("x"))
        y = float(node.get("y"))
        w = float(node.get("width"))
        h = float(node.get("height"))
        self.out("ctx.rect(%.2f, %.2f, %.2f, %.2f);" % (x, y, w, h))
        pass
    
    def draw_path(self, node):
        """Draws svg:path elements"""
        path = parsePath(node.get("d"))
        for pt in path:
            if pt[0] == "M":
                self.out("ctx.moveTo(%.2f, %.2f);" % (pt[1][0], pt[1][1]))
            elif pt[0] == "L":
                self.out("ctx.lineTo(%.2f, %.2f);" % (pt[1][0], pt[1][1]))
            elif pt[0] == "C":
                x1, y1, x2, y2 = pt[1][0], pt[1][1], pt[1][2], pt[1][3]
                x, y = pt[1][4], pt[1][5]
                comm = "ctx.bezierCurveTo(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f);"
                self.out(comm % (x1, y1, x2, y2, x, y))

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

            #finish the path
            if style.has_key("stroke") and style["stroke"] != "none":
                self.out("\nctx.stroke();")

            if style.has_key("fill") and style["fill"] != "none":
                self.out("\nctx.fill();")

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
