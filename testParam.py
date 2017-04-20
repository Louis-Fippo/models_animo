"""
		This file ami to test the package 
		argparse in the aim of use it the 
		projet of converting ANIMO models 
		in IMITATOR models
"""

#import the packages
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", type = help, int="increase output verbosity", action="store_true")
args = parser.parse_args()

if args.verbose:

    print("verbosity turned on")


