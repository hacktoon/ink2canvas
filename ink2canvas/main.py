#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Copyright (C) 2012 Karlisson Bezerra, contact@hacktoon.com

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

from lib import inkex
from canvas import Canvas
import svg

log = inkex.debug  #alias to debug method


class Ink2Canvas(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.canvas = None

    def output(self):
        import sys
        content = self.canvas.output()
        sys.stdout.write(content.encode("utf-8"))

    def get_tag_name(self, node):
        # remove namespace part from "{http://www.w3.org/2000/svg}elem"
        return node.tag.split("}")[1]

    def get_gradient_def(self, elem):
        if not elem.has_gradient():
            return None
        url_id = elem.get_gradient_href()
        # get the gradient element
        gradient = self.xpathSingle("//*[@id='%s']" % url_id)
        # get the color stops
        url_stops = gradient.get(inkex.addNS("href", "xlink"))
        gstops = self.xpathSingle("//svg:linearGradient[@id='%s']" % url_stops[1:])
        colors = []
        for stop in gstops:
            colors.append(stop.get("style"))
        if gradient.get("r"):
            return svg.RadialGradientDef(gradient, colors)
        else:
            return svg.LinearGradientDef(gradient, colors)

    def get_clip_def(self, elem):
        clip_id = elem.get_clip_href()
        return self.xpathSingle("//*[@id='%s']" % clip_id)

    def is_clone(self, node):
        href = node.get(inkex.addNS("href", "xlink"))
        return bool(href)

    def get_clone(self, node):
        href = node.get(inkex.addNS("href", "xlink"))
        clone = self.xpathSingle("//*[@id='%s']" % href[1:])
        return clone

    def walk_tree(self, root, is_clip=False):
        for node in root:
            tag = self.get_tag_name(node)
            class_name = tag.capitalize()

            #if there's not an implemented class, continues
            if not hasattr(svg, class_name):
                continue
            # creates a instance of 'elem'
            # similar to 'elem = Rect(tag, node, ctx)'
            elem = getattr(svg, class_name)(tag, node, self.canvas)
            
            if self.is_clone(node):
                clone = self.get_clone(node)
                if (elem.has_transform()):
                    trans_matrix = elem.get_transform()
                    self.canvas.transform(*trans_matrix)
                self.walk_tree([clone])
                continue
            
            gradient = self.get_gradient_def(elem)
            elem.start(gradient)
            
            #render only the 'first level' elements in a clipping area
            if not is_clip and elem.has_clip():
                clippath = self.get_clip_def(elem)
                self.canvas.beginPath()
                if (elem.has_transform()):
                    self.canvas.save()
                    trans_matrix = elem.get_transform()
                    self.canvas.transform(*trans_matrix)
                self.walk_tree(clippath, True)
                if (elem.has_transform()):
                    self.canvas.restore()
                self.canvas.clip()
            
            #clipping elements are drawn differently
            elem.draw(is_clip)
            self.walk_tree(node, is_clip)
            elem.end()

    def effect(self):
        """Applies the effect"""
        svg_root = self.document.getroot()
        width = inkex.unittouu(svg_root.get("width"))
        height = inkex.unittouu(svg_root.get("height"))
        self.canvas = Canvas(width, height)
        self.walk_tree(svg_root)


if __name__ == "__main__":
    ink = Ink2Canvas()
    ink.affect()
