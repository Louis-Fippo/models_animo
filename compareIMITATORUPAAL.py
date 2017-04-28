#!/usr/bin/python2.7
#-*- coding: utf-8 -*-


"""
* Python program to compare Model checking between IMITATOR and UPAAL of 
ANIMO models

Name          : compareIMITATORUPAAL.py
Version       : 0.0
Author        : Louis Fippo Fitime

Created       : 2017/04/19
Last modified : 2017/04/20


"""

#importation of bibliothèques

import os        
import re             #pour la gestion des expressions régulières
import glob           #pour la concatenation des fichiers
import argparse       #pour parser les arguments de la ligne de commande
import numpy as np    #aussi pour les stats
import pandas as pd   #pour les stat sous python
import fileinput     
#from ggplot import *  #pour le tracé des courbes


#ggplot pour les courbes


#http://pandas.pydata.org/pandas-docs/stable/dsintro.html
#https://docs.python.org/3.1/library/re.html
#expressions regulière diverses, bon à savoir
#http://python.jpvweb.com/python/mesrecettespython/doku.php?id=divers_expr_reg

#program arguments mangement

parser = argparse.ArgumentParser()

#add of options
parser.add_argument("-v", "--verbose", help = "increase output verbosity", action = "store_true")
parser.add_argument("-c", "--compare",  action = "store_true", help = "compare the model checking between IMITATOR and UPAALL on ANIMO models")

#parse options
args = parser.parse_args()



#start

if args.compare:

    #dataframe for concentration
    dataConcen = open("modelesImi/dataConcentration.txt","a")
    etatConcen = open("modelesImi/aetatConcentration.conca","a")
    #read files
    fichier = open("modelesImi/testConcentrations-statespace.states","r")

    concentration = fichier.read()
    nextLigneGood = False #to know if the next ligne contains automata and clocks
    firstLine = True #to check if we need to add the components 
    #quelques motifs pour les expressions régulières
    motifEntier = r"[+-]?[0-9]+"
    motifReel = r"[+-]?(([0-9]+[eE][+-]?[0-9]+)|([0-9]+\.[0-9]*([eE][+-]?[0-9]+)?)|(\.[0-9]+([eE][+-]?[0-9]+)?))"
    ETAT = r"(?P<STATE>STATE)"
    concentrationl = concentration.split("\n")

    
    etatConcen.write("automates"+"\t")


    #var i to determine if is the first case
    for ligne in concentrationl:

		#extract states, clocks and clocks values


		modex = re.search(r"(?P<STATE>STATE) (?P<etat>\d+)",ligne)
		       
		if modex is not None:
		    print ligne     
		    nextLigneGood = True 
		    print modex.group('STATE')
		    print modex.group('etat')
		    etatConcen.write(modex.group('etat')+"\t")
		#   lignedata = lignedata + modex.group('etat')+"\t"
		    

		
		else:
		    if nextLigneGood:
			
			print "is the next ligne:"+ligne
			sligne = ligne.split(",")
			for sl in sligne:
			     print "is sl:"+sl
			     
			     #for real number please update with the formula above
			     modexbis = re.search(r"(?P<automate>\w+) = (?P<clockP>.*) \(~ (?P<clock>.*)\)", sl)
		       
			     if modexbis is not None:
				   print modexbis.groups()
				   print modexbis.group('automate')
				   print modexbis.group('clock')
				   if firstLine :
				       with open("modelesImi/automate"+modexbis.group('automate')+".conca", "a") as automate:
				          automatelec = open("modelesImi/automate"+modexbis.group('automate')+".conca", "r")
				          if len(automatelec.read()) == 0:
					    automate.write(modexbis.group('automate')+"\t")
					    automate.write(modexbis.group('clock')+"\t")
					    automate.close()
					  else:
					    automate.write(modexbis.group('clock')+"\t")
					    automate.close()

					    ligneheader = modexbis.group('automate')+"\t"+modexbis.group('clock')+"\t"
		                   #        lignedata = lignedata + "\t"+modexbis.group('clock')+"\t"
				   else:
					with open("modelesImi/automate"+modexbis.group('automate')+".conca","a") as automate:
					     automate.write(modexbis.group('clock')+"\t")
					     automate.close()
					     ligneheader = "\t"+modexbis.group('clock')+"\t"
				#	     lignedata = lignedata + "\t" + modexbis.group('clock')+"\t"

				  
			     nextLigneGood = False

                    
	    #build a dataframe to plot results
    etatConcenLec = open("modelesImi/aetatConcentration.conca","r")
    etatConcen.close()
    etatConcenLec.close()

    #with concatenate the file 

    model_files = glob.glob("modelesImi/*.conca")
    model_files.sort()

    #concatenation des fichiers
    #il faudra les mettre dans le bon ordre avant
    for f in model_files:
        with open(f,"ra") as infile: 
            dataConcen.write(infile.read()+"\n")
	    print infile.read()
    #fermeture des fichiers
    dataConcen.close()
    

    #toute cette partie est à terminée plu tard
    #read the data file with pandas for statistical analysis
    """
    donnees = pd.read_table("modelesImi/dataConcentration.txt",sep="\t")
    print(donnees.head())
    #delete the last column
    donnees.drop(donnees.columns[[-1]],axis=1, inplace=True)
    donnees.plot()
    #tracé des courbes avec ggplot
    """
    
