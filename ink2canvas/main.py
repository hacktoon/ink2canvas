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

import inkex
from canvas import Canvas
import svg
import sys

log = inkex.debug  #alias to debug method

 
class Ink2Canvas(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.canvas = None

    def output(self):
        content = self.canvas.output()
        sys.stdout.write(content.encode("utf-8"))

    def getNodeTagName(self, node):
        # remove namespace part from "{http://www.w3.org/2000/svg}elem"
        return node.tag.split("}")[1]

    def getGradientDef(self, elem):
        if not elem.has_gradient():
            return None
        gradientHref = elem.get_gradient_href()
        
        # get the gradient element
        gradient = self.xpathSingle("//*[@id='%s']" % gradientHref)
        
        # get the color stops
        colorStops = gradient.get(inkex.addNS("href", "xlink"))
        
        colorStopsNodes = self.xpathSingle("//svg:linearGradient[@id='%s']" % colorStops[1:])
        
        colors = []
        for color in colorStopsNodes:
            colors.append(color.get("style"))
        if gradient.get("r"):
            return svg.RadialGradientDef(gradient, colors)
        else:
            return svg.LinearGradientDef(gradient, colors)

    def getClipDef(self, elem):
        clipId = elem.get_clip_href()
        return self.xpathSingle("//*[@id='%s']" % clipId)

    def isCloneNode(self, node):
        cloneHref = node.get(inkex.addNS("cloneHref", "xlink"))
        return bool(cloneHref)

    def getCloneNode(self, node):
        cloneHref = node.get(inkex.addNS("cloneHref", "xlink"))
        clone = self.xpathSingle("//*[@id='%s']" % cloneHref[1:])
        return clone

    def walkInSVGNodes(self, rootNode, isClip=False):
        for childNode in rootNode:
            tagName = self.getNodeTagName(childNode)
            className = tagName.capitalize()

            #if there's not an implemented class, continues
            if not hasattr(svg, className):
                continue
            # creates a instance of 'element'
            # similar to 'element = Rect(tagName, childNode, ctx)'
            element = getattr(svg, className)(tagName, childNode, self.canvas)
            
            if self.isCloneNode(childNode):
                cloneNode = self.getCloneNode(childNode)
                if (element.has_transform()):
                    transMatrix = element.get_transform()
                    self.canvas.transform(*transMatrix)
                self.walkInSVGNodes([cloneNode])
                continue
            
            gradient = self.getGradientDef(element)
            element.start(gradient)
            
            #render only the 'first level' elements in a clipping area
            if not isClip and element.has_clip():
                clipPath = self.getClipDef(element)
                self.canvas.beginPath()
                if (element.has_transform()):
                    self.canvas.save()
                    transMatrix = element.get_transform()
                    self.canvas.transform(*transMatrix)
                self.walkInSVGNodes(clipPath, True)
                if (element.has_transform()):
                    self.canvas.restore()
                self.canvas.clip()
            
            #clipping elements are drawn differently
            element.draw(isClip)
            self.walkInSVGNodes(childNode, isClip)
            element.end()

    def effect(self):
        """Applies the effect"""
        svgRoot = self.document.getroot()
        width = inkex.unittouu(svgRoot.get("width"))
        height = inkex.unittouu(svgRoot.get("height"))
        self.canvas = Canvas(width, height)
        self.walkInSVGNodes(svgRoot)


if __name__ == "__main__":
    ink = Ink2Canvas()
    ink.affect()