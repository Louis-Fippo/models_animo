
#-*- coding: utf-8 -*-


"""
* Python program to compare Model checking between 
UPPAAL and IMITATOR

Name          : tracer.py
Version       : 0.0
Author        : Louis Fippo Fitime

Created       : 2017/05/09
Last modified : 2017/05/09


"""

#importation of bibliothèques

import sys
import os        
import argparse       #pour parser les arguments de la ligne de commande
import numpy as np    #aussi pour les stats
import pandas as pd   #pour les stat sous python
import matplotlib.pyplot as plt
import fileinput     

plt.style.use('ggplot')


#read the data file with pandas for statistical analysis
    
donnees = pd.read_table("modelesImi/data/dataConcentrationbis.txt",sep="\t")
print(donnees.head())
donnees = donnees.drop('Unnamed: 3', axis=1) #delete the last column
print(donnees.head())
donnees.plot();
save("concentration", ext="png", close=False, verbose=True)
#tracé des courbes avec ggplot
    
