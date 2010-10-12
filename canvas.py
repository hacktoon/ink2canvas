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

    def out(self, text):
        """Stores text to be written to a file later"""
        self.code += text + "\n"

    def set_color(self, rgb, a):
        """Returns a rgba set"""
        rgb = rgb[1:]  # removes the '#'
        r = int(rgb[:2], 16)
        g = int(rgb[2:4], 16)
        b = int(rgb[4:], 16)
        a = float(a)
        if a == 1.0:
            return "'rgb(%d, %d, %d)';" % (r, g, b)
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

    def effect(self):
        """Applies the effect"""
        
        self.out("ctx = canvas.getContext(\"2d\");")

        for nid, node in self.selected.iteritems():
            self.out("// " + node.get("id"))
            self.out("ctx.beginPath();\n")

            #parse the element style properties into a dictionary
            style = parseStyle(node.get("style"))
            self.set_style(style)

            #start the drawing
            path = parsePath(node.get("d"))
            for p in path:
                if p[0] == "M":
                    self.out("ctx.moveTo(%d, %d);" % (p[1][0], p[1][1]))
                elif p[0] == "L":
                    self.out("ctx.lineTo(%d, %d);" % (p[1][0], p[1][1]))

            #finish the path
            if style.has_key("stroke"):
                self.out("\nctx.stroke();")

            if style.has_key("fill"):
                self.out("\nctx.fill();")

            self.out("\nctx.closePath();")

            #reseting globalAlpha value
            if style.has_key("opacity") and float(style["opacity"]) < 1:
                self.out("ctx.globalAlpha = 1;")

            #if node.tag == inkex.addNS("text", "svg"):

        f = open("canvas.js", "w")
        f.write(self.code)
        f.close()

b = Canvas()
b.affect()
