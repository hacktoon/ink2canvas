'''
Created on 16/05/2012

@author: tasso
'''

class Root(object):

    def __init__(self):
        self.drawable = []
        self.clipPath = {}
        self.linearGradient = {}
        self.radialGradient = {}

    def addChildDrawable(self, child):
        self.drawable.append(child)

    def addChildClipPath(self, key, value):
        self.clipPath[key] = value;

    def addChildLinearGradient(self, key, value):
        self.clipPath[key] = value;

    def addChildRadialGradient(self, key, value):
        self.clipPath[key] = value;
    
    def getDrawable(self):
        return self.drawable

    def getClipPath(self, key):
        return self.clipPath[key]

    def getLinearGradient(self, key):
        return self.linearGradient[key]

    def getRadialGradient(self, key):
        return self.radialGradient[key]




