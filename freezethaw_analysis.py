#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freezethaw_analysis.py - Analyzing temperature data for Paamiut, Greenland for 
ENVS 80.01, Arctic Environmental Change

Analyzing temperature data to understand the future of a potato farming industry
in Greenland due to the warming climate. In this script, I want to calculate 
the number of "thaw freeze" events; where the temperature goes above freezing for
at least a day and then goes below freezing again. We need to know how the number
of these events is changing on a yearly basis as potatoes can't grow under these
conditions.

Author: Sam Morton
January 31, 2020
"""


import pandas as pd


TMAX_FLAG_LOC = 4
TMIN_FLAG_LOC = 6


def data_check(df, idx):
    '''
    Verify if a data row is valid. Data is invalid either if there is missing
    data or if the temperature flags are present in the list of unacceptable 
    flags. Returns True if the data row is valid, False otherwise.
    df - the DataFrame
    idx - the index of the row to be checked
    '''
    
    # first verify that the temperature flags are acceptable
    tmax_flags = df.iloc[i, TMAX_FLAG_LOC]
    tmin_flags = df.iloc[i, TMIN_FLAG_LOC]
    
    if len(tmax_flags) == 0 or len(tmin_flags) == 0:
        return False
    
    
    



'''
#=== Example of how to open an Excel file using Pandas ===
df = pd.read_excel('data/paamiut_tempdata.xlsx', sheet_name = '2016157')
print(len(df.iloc[0, 4]))
print(len(""))
#for i in df.index:
'''



