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
import re
import argparse
import numpy as np
import pandas as pd

#ggplot pour les courbes


#http://pandas.pydata.org/pandas-docs/stable/dsintro.html



#program arguments mangement

parser = argparse.ArgumentParser()

#add of options
parser.add_argument("-v", "--verbose", help = "increase output verbosity", action = "store_true")
parser.add_argument("-c", "--compare",  action = "store_true", help = "compare the model checking between IMITATOR and UPAALL on ANIMO models")

#parse options
args = parser.parse_args()



#start

if args.compare:

    #read files
    fichier = open("modelesImi/testConcentrations-statespace.states","r")

    concentration = fichier.read()

    ETAT = r"(?P<STATE>\w+)"
    concentrationl = concentration.split("\n")
    for ligne in concentrationl:

     #extract states, clocks and clocks values

        modex = re.search(r"(?P<STATE>\w+) (?P<etat>\d+)",ligne)
               
        if modex is not None:
       
            print modex.group('STATE')
	    print modex.group('etat')
	
	else:
	    sligne = ligne.split(",")
	    for sl in sligne:

	       modexbis = re.search(r"(?P<automate>\w+) = d+|d+/d+ (~(?P<clock>\d+.d+))", sl)
               
	       if modexbis is not None:

	           print modexbis.group('automate')
	           print modexbis.group('etat')





    #build a dataframe to plot results

 


