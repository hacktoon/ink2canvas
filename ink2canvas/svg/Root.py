'''
Created on 16/05/2012

@author: tasso
'''

from ink2canvas.svg.G import G

class Root(object):

    def __init__(self):
        self.drawable = []
        self.clipPath = {}
        self.linearGradient = {}
        self.radialGradient = {}

    def searchElementById(self,idQueTenhoQueAchar,nosQueDevemSerDesenhados):
        retorno = None
        for noEmQuestao in nosQueDevemSerDesenhados:
            if(noEmQuestao.getId() == idQueTenhoQueAchar):
                return noEmQuestao
            if(isinstance(noEmQuestao, G)):
                retorno = self.searchElementById(idQueTenhoQueAchar, noEmQuestao.children)
                if(retorno!=None):
                    break
        return retorno

    def addChildDrawable(self, child):
        self.drawable.append(child)

    def addChildClipPath(self, key, value):
        self.clipPath[key] = value;

    def addChildLinearGradient(self, key, value):
        self.linearGradient[key] = value;

    def addChildRadialGradient(self, key, value):
        self.radialGradient[key] = value;
    
    def getDrawable(self):
        return self.drawable

    def getClipPath(self, key):
        return self.clipPath[key]

    def getLinearGradient(self, key):
        return self.linearGradient[key]

    def getRadialGradient(self, key):
        return self.radialGradient[key]




