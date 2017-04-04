#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob

from lxml import etree


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







model = open("model.imi","wra")

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
automata.write("--automata   \n\n")


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

#print node id

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
       variables_clock.write("x_"+node.text)
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

#Parametr constraints
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







#petit test pour effecer dans un fichier





#fermeture des sous fichiers
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


