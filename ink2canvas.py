#!/usr/bin/env python
'''
Copyright (C) 2011 Karlisson Bezerra, contato@nerdson.com

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
from lib.canvas import Canvas
import lib.svg as svg

log = inkex.debug  #alias to debug method


class Ink2Canvas(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.canvas = None

    def output(self):
        import sys
        sys.stdout.write(self.canvas.output())

    def get_defs(self, elem):
        if elem.has_gradient():
            pass

    def walk_tree(self, root):
        for node in root:
            # remove namespace part from "{http://www.w3.org/2000/svg}elem"
            tag = node.tag.split("}")[1].capitalize()
            if not hasattr(svg, tag):
                continue
            # creates a instance of 'elem'
            # similar to 'elem = Rect(tag, node, ctx)'
            elem = getattr(svg, tag)(tag, node, self.canvas)
            defs = self.get_defs(elem)
            elem.start(defs)
            elem.draw()
            self.walk_tree(node)
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
