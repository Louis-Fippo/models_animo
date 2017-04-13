#!/usr/bin/env python
# -*- coding: utf-8 -*-



#class pour construire un graph 
#à partir du fichier xml d'animo

#class graphe ***************************************

#class Molecule: pour representer les molecules d un modele

class Molecule:
   #class molécule contenant
   #contenant les attributs suivants
   #les attributs
   #  SUID = ""
   # selected = true
   # canonicalName = ""


    def __init__(self,SUIDp,selectedp,canonicalNamep,initialConcentrationp,levelsp,moleculeTypep):
      #constructeur
        self.SUID = SUIDp
        self.selected = selectedp
        self.canonicalName = canonicalNamep
        self.initialConcentration = initialConcentrationp
        self.levels = levelsp
        self.moleculeType = moleculeTypep
        self.succ = []  #structure dictionnaire? {mol:mol1,influ:act|inh}
        self.pred = []  #idem

    def getSUID(self):

        return self.SUID

    def getName(self):

        return self.canonicalName

    def getSelected(self):

        return self.selected

#fin Molecule*******************************************


#class Interaction: pour les interactions d un modele
class Interaction:
  #class Interaction pour caractériser 
  #les interactions entre les composants
  #d un modele

    def __init__(self,source,target,SUID,selected,increment,k,activityRatio):
      #constructeur
        self.source = source
        self.target = target
        self.SUID = SUID
        self.selected = selected
        self.increment = increment
        self.k = k
        self.activityRatio = activityRatio

    def getSource(self):

        return self.source

    def getTarget(self):

        return self.target

    def getSUID(self):

        return self.SUID

    def getIncrement(self):

        return self.increment


#fin Interaction****************************************


class Graph:

    def __init__(self):

     #constructeur
       self.nodes = []
       self.edges = []

    def size(self):

       return len(self.nodes)


    def addNode(self, noeud):

       self.nodes.append(noeud)

    def getNode(self,ID):

       for n in  self.nodes:
         if n.SUID == ID:
           return n

    def printNodes(self):

        for n in self.nodes:
          print(n.canonicalName)


    def addEdge(self, edge):

       self.edges.append(edge)

    def getSucc(self, noeud):

       succ = [] #initialisation de la liste des successeurs

       #selection de tous les arcs qui ont pour source le noeud
       for e in self.edges:
         if noeud.SUID == e.source:
            nt = self.getNode(e.target)
            succ.append(nt)
       return succ

    def getPred(self, noeud):

        pred = [] #initialisation de la liste des predecesseurs

        #sélection de tous les arcs qui ont pour target le noeud
        for e in self.edges:
          if noeud.SUID == e.target:
             nt = self.getNode(e.source)
             pred.append(nt)
        return pred
#Methods on edges

    def activation(self, source, target):

         act = False
         for e in self.edges:
           if ((e.source == source) & (e.target == target)):
              if e.increment == "1":
                 act = True
         return act

#*****************************************************


#definition of some important fucntion

def getPred(model):
     #fonction pour extriate les prédecesseur d'un noeud

    for edge in model.xpath("/graphml/graph/edge"):
        target = edge.get("target")
        PredTarget = []
        for edge in tree.xpath("/graphml/graph/edge"):
            if edge.get("target") == target :
               PredTarget.append(edge.get("source"))

    return PredTarget
#end of getPred


def getSucc(model):
     #function to get succesor of a node

    for edge in model.xpath("/graphml/graph/edge"):
        source = edge.get("source")
        SuccSource = []
        for edge in tree.xpath("/graphml/graph/edge"):
            if edge.get("source") == source:
               SuccSource.append(edge.get("target"))

    return SuccSource
#end of getSucc


def getName(model, noeud):
    #to get the name of a node

    return 0


def getText(cle):

    optionText = { "SUID":66,
                   "name":node,
                   "levels":100,
                 }

#fin définition des fonctions *****************************************






