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

import sys
import inkex
from canvas import Canvas
from Ink2CanvasCore import Ink2CanvasCore
 
class Ink2Canvas(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.core = Ink2CanvasCore(inkex, self)


    def effect(self):
        svgRoot = self.document.getroot()
        
        tmpWidth = svgRoot.get("width")
        if tmpWidth == None:        
            width = self.unittouu("800")
        else:
            width = self.unittouu(tmpWidth)
            
        tmpHeight = svgRoot.get("height")
        if tmpHeight == None:
            height = self.unittouu("600")
        else:
            height = self.unittouu(tmpHeight)
            
        self.core.canvas = Canvas(width, height)
        self.core.createTree(svgRoot)
        for drawable in self.core.root.getDrawable():
            drawable.runDraw()

    def output(self):
        content = self.core.canvas.output()
        sys.stdout.write(content.encode("utf-8"))

    
if __name__ == "__main__":
    i2c = Ink2Canvas()
    i2c.affect()

