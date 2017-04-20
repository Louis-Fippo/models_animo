#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import argparse
from graphTools.graph import *
from lxml import etree



#gestion des arguments 
parser = argparse.ArgumentParser()

parser.add_argument("-p","--parameters", help = "parameters to be estimated", action = "store_true")
parser.add_argument("-m","--mode", help = "chose the cooperation mode between many component having a concurrent action", action = "store_true")
parser.add_argument("-i","--model",  help = "input model", action = "store_true")
parser.add_argument("-v","--verbose", help="increase output verbosity", action = "store_true")
args = parser.parse_args()

if args.model:

	model = open("model_fit_egf.imi","wra")
	
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





	tree = etree.parse("modelesBio/Model_fit_egf.xml")
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

		  mol.canonicalName = f.text.replace(" ","_")
	   
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
	    automata.write("synclabs: "+"activate"+node.canonicalName+", inhibate"+node.canonicalName)
	    #ajouter les synclab basé sur les successeurs
	    syncact = ""
	    syncinh = ""
	    for suc in modelGraph.getSucc(node):
	      if modelGraph.activation(node.SUID,suc.SUID):
		automata.write(", activate"+suc.canonicalName)
		syncact = syncact+",activate"+suc.canonicalName
	      else:
		automata.write(", inhibate"+suc.canonicalName)
		syncinh = syncinh+",inhibate"+suc.canonicalName
	    
	    automata.write(";\n\n")
            syncact.split(",")
	    for elt in syncact.split(","):

                print("syncact",elt)
	    

	    #ajout des transitions
	    #loc inactive
	    automata.write("loc "+"inactive_"+node.canonicalName+": while True wait {} \n")
	    automata.write("          when True  sync activate"+node.canonicalName+" do {x_"+node.canonicalName+"' = 0} goto activating_"+node.canonicalName+";\n\n")
	    
	    
	    #loc activating
	    automata.write("loc "+"activating_"+node.canonicalName+": while x_"+node.canonicalName+" <= d_"+node.canonicalName+"_max wait {} \n")
            automata.write("            when x_"+node.canonicalName+" >= d_"+node.canonicalName+"_min do {x_"+node.canonicalName+"' = 0} goto active_"+node.canonicalName+"; \n")
	    for elt in syncact.split(","):
	      if elt!= "":
	         automata.write("            when x_"+node.canonicalName+" >= d_"+node.canonicalName+"_min  sync "+elt+" do {x_"+node.canonicalName+"' = 0} goto active_"+node.canonicalName+"; \n")   
            
	    #loc inhibiting
	    automata.write("\n")
	    automata.write("loc "+"inhibiting_"+node.canonicalName+": while x_"+node.canonicalName+" >= d_"+node.canonicalName+"_min wait {}\n")
            automata.write("           when x_"+node.canonicalName+" < d_"+node.canonicalName+"_max do {x_"+node.canonicalName+"' = 0} goto inactive_"+node.canonicalName+"; \n")
	    for elt in syncinh.split(","):
	       if elt != "":
	          automata.write("            when x_"+node.canonicalName+" < d_"+node.canonicalName+"_max  sync "+elt+" do {x_"+node.canonicalName+"' = 0} goto inactive_"+node.canonicalName+"; \n\n")    

            
	    #loc active
	    automata.write("\n")
	    automata.write("loc "+"active_"+node.canonicalName+": while True wait {} \n")
	    automata.write("            when True sync inhibate"+node.canonicalName+" do {x_"+node.canonicalName+"' = 0} goto inhibiting_"+node.canonicalName+";\n\n")
	    

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





	#fermeture des sous fichiers  ***********************************************
	variables_clock.write(": clock; \n\n")
	variables_param.write("\n")
	variables_param.write("                    : parameter; \n\n")
	init_param.write("\n;")
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


