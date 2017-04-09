#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob

#import graphTools.graph

from lxml import etree

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





model = open("modelABCDE.imi","wra")

#head of file
model.write("(********************************************************\n\n")
model.write("*              IMITATOR MODEL                          \n\n")
model.write("*Description: ?   \n")
model.write("*Correctness: ? \n")
model.write("*Source: ?\n")
model.write("*Author: ?\n")
model.write("*Modeling: Louis Fippo Fitime \& Etienne André\n")
model.write("*Input by: Louis Fippo Fitime\n")
model.write("*Licence: Creative Commons ...\n")
model.write("*  \n")
model.write("*Created : \n")
model.write("*Last modified : \n")
model.write("*   \n")
model.write("* IMITATOR version : 2.9 \n")  
model.write("***********************************************************)\n\n")
model.write("--model"+"\n\n\n")


#comment déterminer automatiquement le nombre d'horloge?
#pour l'instant, je vais mettre une horloge par composant
variables_clock = open("avariables_clock.imi","wra")
variables_clock.write("var \n\n ")
variables_clock.write("(* Clocks *)\n")

variables_param = open("avariables_param.imi","wra")
variables_param.write("(* Parameters *)\n")

automata = open("inautomata.imi","wra")
automata.write("--automata new   \n\n")


#initialisation
init = open("initial_a.imi","wra")
init.write("(**************************************************)\n")
init.write("(* Initial state *)\n")
init.write("(**************************************************)\n")
init.write("init := \n")

#initial location
init_loc = open("initial_aloc.imi","wra")
init_loc.write("(*---------------------------------------------*)\n")
init_loc.write("(* Initial location *)\n")
init_loc.write("(*---------------------------------------------*)\n")


#initial clock constraints
init_clock = open("initial_clock.imi","wra")
init_clock.write("\n(*---------------------------------------------*)\n")
init_clock.write("(* Initial clock constraints *)\n")
init_clock.write("(*---------------------------------------------*)\n")


#parameters  constraints
init_param = open("initial_param.imi","wra")
init_param.write("\n(*---------------------------------------------*)\n")
init_param.write("(* Parameter constraints *)\n")
init_param.write("(*---------------------------------------------*)\n")





tree = etree.parse("data.xml")
modelGraph = Graph()

#construction d'une structure de donné pour stocker le graphe
mol = Molecule("","","","","","")

nombreNoeudAjoute = 0

for nodetemp in tree.xpath("/graphml/graph/node"):
   
   mol = Molecule("","","","","","")
   fils =  nodetemp.getchildren()
   for f in fils:
      if f.get("key") == "SUID":
   
          mol.SUID = f.text
   
      if f.get("key") == "canonicalName":

          mol.canonicalName = f.text
   
      if f.get("key") == "selected":
  
          mol.selected = f.text
  
      if f.get("key") == "moleculeType":
  
          mol.moleculeType = f.text

      if f.get("key") == "initialConcentration":

          mol.initialConcentration = f.text

      if f.get("key") == "levels":
 
          mol.levels = f.text

#ajout d un noeud dans le graphe

   modelGraph.addNode(mol)
   nombreNoeudAjoute = nombreNoeudAjoute + 1

 
   print("mol.canonical name "+mol.canonicalName)
   print("mol.SUID "+mol.SUID)
   print("mol.levels "+mol.levels)
   print("taille du graphe: ",modelGraph.size())
   print("nombre de noeud ajouté: ",nombreNoeudAjoute)
         
#ajout des arcs dans le graph

inter = Interaction("","","","","","","")

for edgetemp in tree.xpath("/graphml/graph/edge"):

   inter = Interaction("","","","","","","")
   inter.source = edgetemp.get("source")
   inter.target = edgetemp.get("target")
   fils =  edgetemp.getchildren()
   for f in fils:
      if f.get("key") == "SUID":

          inter.SUID = f.text
 
      if f.get("key") == "selected":

          inter.selected = f.text
 
      if f.get("key") == "increment":
   
          inter.increment = f.text

      if f.get("key") == "k":

          inter.k = f.text

      if f.get("key") == "activityRatio":

          inter.activityRatio = f.text       

   modelGraph.addEdge(inter)
   print("inter.source  "+inter.source)
   print("inter.SUID "+inter.SUID)
   print("inter.increment "+inter.increment)
   print("taille du graphe en edge: ",modelGraph.size())
    

#nouvelle version avec les graphes

modelGraph.printNodes()


#compteur pour les virgules
compteur = 0

for node in modelGraph.nodes:
    print("dans la nouvelle construction du model"+node.SUID)
    print(node.canonicalName)
#on ecrit les horloges
    if compteur != 0:
       variables_clock.write(",")
       variables_param.write(", \n")
    compteur=compteur + 1
    variables_clock.write(" x_"+node.canonicalName)
    variables_param.write("d_"+node.canonicalName+"_min,"+" d_"+node.canonicalName+"_max")
#les automates
    automata.write("(***************************************)\n")
    automata.write("  automaton "+node.canonicalName+ "\n")
    automata.write("(***************************************)\n")
    automata.write("synclabs: "+"activate"+node.canonicalName)
    #ajouter les synclab basé sur les successeurs
    for suc in modelGraph.getSucc(node):
      automata.write(", activate"+suc.canonicalName)
    
    automata.write(";\n\n")
    #ajout des transitions
    automata.write("loc "+"inactive_"+node.canonicalName+":  \n\n")
    automata.write("loc "+"activating_"+node.canonicalName+":  \n\n")
    automata.write("loc "+"active_"+node.canonicalName+":  \n\n")
    automata.write("end (* "+node.canonicalName+" new*)\n\n\n")
    print("nous sommes ici")
#initialisation des horloges
    init_clock.write("& x_"+node.canonicalName+" = 0 \n")

#Parameter constraints
    init_param.write("& 0 <= d_"+node.canonicalName+"_min & d_"+node.canonicalName+"_min <= d_"+node.canonicalName+"_max \n")

    if node.initialConcentration == "0":
       init_loc.write("& loc ["+node.canonicalName+"] = inactive_"+node.canonicalName+"\n")
    else:
       init_loc.write("& loc ["+node.canonicalName+"] = active_"+node.canonicalName+"\n")










#compteur pour les virgules
compteur = 0

for node in tree.xpath("/graphml/graph/node/data"):
    print(node.get("key"))
    print(node.text)
#on ecrit les horloges
    if node.get("key")== "canonicalName":
       if compteur != 0:
          variables_clock.write(",")
          variables_param.write(", \n")
       compteur=compteur + 1 
       variables_clock.write(" x_"+node.text)
       variables_param.write("d_"+node.text+"_min,"+" d_"+node.text+"_max")
#les automates
       automata.write("(***************************************)\n")
       automata.write("  automaton "+node.text+ "\n")
       automata.write("(***************************************)\n")
       automata.write("synclabs: "+"\n") 
       automata.write("\n")
       automata.write("loc "+"inactive_"+node.text+":  \n\n")
       automata.write("loc "+"activating_"+node.text+":  \n\n")
       automata.write("loc "+"active_"+node.text+":  \n\n")
       automata.write("end (* "+node.text+" *)\n\n\n")
#initialisation des horloges
       init_clock.write("& x_"+node.text+" = 0 \n")

#Parameter constraints
       init_param.write("& 0 <= d_"+node.text+"_min & d_"+node.text+"_min <= d_"+node.text+"_max \n")

    if node.get("key")== "initialConcentration":
        if node.text == "0":
           init_loc.write("& loc ["+node.text+"] = inactive_"+node.text+"\n")
        else:
           init_loc.write("& loc ["+node.text+"] = active_"+node.text+"\n")
        

#ajout des locations
#    if node.get("key")== "canonicalName":
#       automata.write("loc "+node.text+"0"+":  \n\n")
#       automata.write("loc "+node.text+"1"+":  \n\n") 

#print edge
for edge in tree.xpath("/graphml/graph/edge"):
    target= edge.get("target")
    PredTarget = [] 
    for edge in tree.xpath("/graphml/graph/edge"):
        if edge.get("target") == target : 
            PredTarget.append(edge.get("source"))
       
    print(getPred(tree))
    print(edge.get("source") +"-----"+edge.get("target"))







#fermeture des sous fichiers  ***********************************************
variables_clock.write(": clock; \n\n")
variables_param.write("\n")
variables_param.write("                    : parameters; \n\n")
variables_clock.close()
variables_param.close()
init_clock.close()
init_loc.close()
init_param.close()
init.close()
automata.close()


model_files = glob.glob("*.imi")
model_files.sort()

#concatenation des fichiers
#il faudra les mettre dans le bon ordre avant
for f in model_files:
 with open(f,"ra") as infile: 
   if f!= "model.imi":
     model.write(infile.read())
     print(f)
   else:
     print "yes"
   

#fermeture des fichiers
model.close()


