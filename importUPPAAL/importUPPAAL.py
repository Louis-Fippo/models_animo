#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob

from lxml import etree


model = open("model.imi","wra")
model.write("--model"+"\n\n\n")


#comment déterminer automatiquement le nombre d'horloge?
#pour l'instant, je vais mettre une horloge par composant
variables = open("variables.imi","wra")
variables.write("var ")

automata = open("automata.imi","wra")
automata.write("--automata   \n\n")


tree = etree.parse("test.xml")


#test de debug
print("Convert from UPPAAL to IMITATOR")


#root

root = etree.Element("root")

print(root.text)

for element in root.iter():
     print("%s - %s" % (element.tag, element.text))

#print node id
for node in tree.xpath("/declaration"):
    print(node.text)
#on ecrit les horloges
#    if node.get("key")== "canonicalName":
#       variables.write("c"+node.text + "," )
#les automates
#       automata.write("--automaton-------------\n")
#       automata.write("automaton "+node.text+ "\n\n")
#       automata.write("synclabs: "+"\n") 
#       automata.write("\n")

#    if node.get("key")== "initialConcentration":
#        if node.text == "0":
#           automata.write("initially "+node.text+"\n\n")
#        else:
#           automata.write("initially "+node.text+"\n\n")

#ajout des locations
#    if node.get("key")== "canonicalName":
#       automata.write("loc "+node.text+"0"+":  \n\n")
#       automata.write("loc "+node.text+"1"+":  \n\n") 

#print edge
#for edge in tree.xpath("/graphml/graph/edge"):
#    print(edge.get("source") +"-----"+edge.get("target"))





#fermeture des sous fichiers
variables. write(": clock; \n")
variables.close()
automata.close()


model_files = glob.glob("*.imi")


#concatenation des fichiers
#il faudra les mettre dans le bon ordre avant
for f in model_files:
 with open(f,"ra") as infile: 
   model.write(infile.read())


#fermeture des fichiers
model.close()


