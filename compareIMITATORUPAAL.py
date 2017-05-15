
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

import sys
import os        
import re             #pour la gestion des expressions régulières
import glob           #pour la concatenation des fichiers
import argparse       #pour parser les arguments de la ligne de commande
import numpy as np    #aussi pour les stats
import pandas as pd   #pour les stat sous python

"""
try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
"""
import matplotlib.pyplot as plt
#import tkinter
import fileinput     

plt.style.use('ggplot')
#sudo pip2 install -U matplotlib --ignore-installed six


#sudo apt-get install python python-tk idle python-pmw python-imaging
#from ggplot import *  #pour le tracé des courbes      sudo apt-get install python-tk python-imaging-tk python3-tk   && apt-cache policy python-tk &&
#sudo apt-get install tk-dev
"""
try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
import matplotlib.pyplot as plt

#ggplot pour les courbes
matplotlib.style.use('ggplot')
"""
#ggplot pour les courbes
#matplotlib.style.use('ggplot')

#http://pandas.pydata.org/pandas-docs/stable/dsintro.html
#http://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/notebooks/td2a_cenonce_session_1.html
#https://docs.python.org/3.1/library/re.html
#expressions regulière diverses, bon à savoir
#http://python.jpvweb.com/python/mesrecettespython/doku.php?id=divers_expr_reg
#http://python3.codes/


#python -m pip install -U pip setuptools
#python -m pip install matplotlib
#sudo apt-get install python-matplotlib
#sudo apt-get build-dep python-matplotlib


#definition of a function to save images
def save(path, ext='png', close=True, verbose=True):
    """Save a figure from pyplot.
    Parameters
    ----------
    path : string
        The path (and filename, without the extension) to save the
        figure to.
    ext : string (default='png')
        The file extension. This must be supported by the active
        matplotlib backend (see matplotlib.backends module).  Most
        backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.
    close : boolean (default=True)
        Whether to close the figure after saving.  If you want to save
        the figure multiple times (e.g., to multiple formats), you
        should NOT close it in between saves or you will have to
        re-plot it.
    verbose : boolean (default=True)
        Whether to print information about when and where the image
        has been saved.
    """
    
    # Extract the directory and filename from the given path
    directory = os.path.split(path)[0]
    filename = "%s.%s" % (os.path.split(path)[1], ext)
    if directory == '':
        directory = '.'

    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # The final path to save to
    savepath = os.path.join(directory, filename)

    if verbose:
        print("Saving figure to '%s'..." % savepath),

    # Actually save the figure
    plt.savefig(savepath)
    
    # Close it
    if close:
        plt.close()

    if verbose:
        print("Done")




#program arguments mangement

parser = argparse.ArgumentParser()

#add of options
parser.add_argument("-v", "--verbose", help = "increase output verbosity", action = "store_true")
parser.add_argument("-c", "--compare",  action = "store_true", help = "compare the model checking between IMITATOR and UPAALL on ANIMO models")

#parse options
args = parser.parse_args()



#start

if args.compare:
    
    #clean temporary directory
    print("Cleanning temporary directory...")
    os.system('rm modelesImi/*.conca')
    os.system('rm modelesImi/data/*.conca')
    os.system('rm modelesImi/data/*.txt')
    os.system('rm modelesImi/dataConcentration.txt')
    print("End of cleanning.")
    print("Building new files...")
    
    #generate data from model checking with IMITATOR
    os.system('./imitator modelesImi/testConcentrations.imi -mode statespace -depth-limit 600 -output-states -output-float')
    print("Fin generation donnees")


    
    #dataframe for concentration
    dataConcen = open("modelesImi/dataConcentration.txt","a")
    dataConcenbis = open("modelesImi/data/dataConcentrationbis.txt","a")
    etatConcen = open("modelesImi/aetatConcentration.conca","a")
    etatConcenbis = open("modelesImi/data/etatConcentrationbis.conca","a")
    automatebis = open("modelesImi/data/automatebis.conca","a")
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
            print(ligne)
            nextLigneGood = True
            print(modex.group('STATE'))
            print(modex.group('etat'))
            etatConcen.write(modex.group('etat')+"\t")
            etatConcenbis.write(modex.group('etat')+"\t")
            #   lignedata = lignedata + modex.group('etat')+"\t"
        else:
            if nextLigneGood:
                print("is the next ligne:"+ligne)
                sligne = ligne.split(",")
                for sl in sligne:
                    print("is sl:"+sl)
                    #for real number please update with the formula above
                    modexbis = re.search(r"(?P<automate>\w+) = (?P<clockP>.*) \(~ (?P<clock>.*)\)", sl)
                    if modexbis is not None:
                        print(modexbis.groups())
                        print(modexbis.group('automate'))
                        print(modexbis.group('clock'))
                        if firstLine :
                            with open("modelesImi/automate"+modexbis.group('automate')+".conca", "a") as automate:
                                automatelec = open("modelesImi/automate"+modexbis.group('automate')+".conca", "r")
                                if len(automatelec.read()) == 0:
                                    automate.write(modexbis.group('automate')+"\t")
                                    automate.write(modexbis.group('clock')+"\t")
                                    automatebis.write(modexbis.group('automate')+"\t") #pour la versionn en colonnes
                                    etatConcenbis.write(modexbis.group('clock')+"\t")
                                    automate.close()
                                    
                                else:
                                    automate.write(modexbis.group('clock')+"\t")
                                    etatConcenbis.write(modexbis.group('clock')+"\t")
                                    automate.close()
                                    ligneheader = modexbis.group('automate')+"\t"+modexbis.group('clock')+"\t"
                                    #        lignedata = lignedata + "\t"+modexbis.group('clock')+"\t"
                        else:
                            with open("modelesImi/automate"+modexbis.group('automate')+".conca","a") as automate:
                                automate.write(modexbis.group('clock')+"\t")
                                etatConcenbis.write(modexbis.group('clock')+"\t")
                                automate.close()
                                ligneheader = "\t"+modexbis.group('clock')+"\t"
                                #	     lignedata = lignedata + "\t" + modexbis.group('clock')+"\t"
                        nextLigneGood = False
                etatConcenbis.write("\n")

                    
	#build a dataframe to plot results
    etatConcenLec = open("modelesImi/aetatConcentration.conca","r")
    etatConcen.close()
    etatConcenLec.close()
    etatConcenbis.close()
    automatebis.close()

    #concatenate the file 

    model_files = glob.glob("modelesImi/*.conca")
    model_files.sort()

    #concatenation des fichiers
    for f in model_files:
        with open(f,"r") as infile: 
            dataConcen.write(infile.read()+"\n")
                
    
    #concatenate files with the second approach
    model_filesbis = glob.glob("modelesImi/data/*.conca")
    model_filesbis.sort()
    
    for f in model_filesbis:
        with open(f,"r") as infile:
            dataConcenbis.write(infile.read()+"\n")
            
        
    
    
    
    #fermeture des fichiers
    dataConcen.close()
    dataConcenbis.close()
    

    #toute cette partie est à terminée plu tard
    #read the data file with pandas for statistical analysis
    
    donnees = pd.read_table("modelesImi/data/dataConcentrationbis.txt",sep="\t")
    print(donnees.head())
    #delete the last column
    #donnees.drop(donnees.columns[[-1]],axis=1, inplace=True)
    donnees = donnees.drop('Unnamed: 3', axis=1)
    print(donnees.head())
    donnees.plot();
    save("concentration", ext="png", close=False, verbose=True)

    #tracé des courbes avec ggplot
    
    
