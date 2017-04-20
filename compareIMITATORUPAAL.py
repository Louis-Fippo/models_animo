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


#program arguments mangement

parser = argparse.ArgumentParser()

#add of options
parser.add_argument("-v", "--verbose", type = string, help = "increase output verbosity", action = "store_true")


#parse options
args = parser.parse_args()



#start

if args.verbose:
   
    print("verbosity turned on")

    #read files
    concentration = open("testConcentrations-statespace.states","ra")

    concentration.


    #extract states, clocks and clocks values



    #build a dataframe to plot results

 


