#!/usr/bin/env python
# -*- coding: utf-8 -*-



#class pour construire un graph 
#à partir du fichier xml d'animo

import os

#class noeud

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


    def getSelected(self):
        
        return self.selected
    
    
