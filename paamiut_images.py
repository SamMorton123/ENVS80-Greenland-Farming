#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Just some code to generate the necessary figure(s) for the project. Wanted to 
split this up from the rest of the code for better organization. 

Sam Morton
February 6, 2020
"""


import numpy as np
import matplotlib.pyplot as plt
import freezethaw_analysis as fta


XLABEL = "Year"
YLABEL = "Number of early spring thaw-freeze events"
TITLE = "Change In the Number of Annual Thaw-Freeze Events Over Time"
XBEGIN = 1955
XEND = 2020
XSTEP = 5
YBEGIN = 0
YEND = 10
YSTEP = 1


def timeseries_image(filename, plot_type = "scatter"):
    '''
    Take the name of Excel data and turn it into a plot.
    data - the name of the Excel file
    plot_type - default plot type set to scatter for now
    '''
    
    # get the thaw_freezes per year
    (years, tfs) = fta.thaw_freeze_main(filename)
    
    if plot_type == "scatter":
        plt.plot(years, tfs, 'o', color = 'black')
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    plt.xticks(np.arange(XBEGIN, XEND + 1, step = XSTEP))
    plt.yticks(np.arange(YBEGIN, YEND + 1, step = YSTEP))
    plt.title(TITLE)
    
    


timeseries_image(fta.DATA)
