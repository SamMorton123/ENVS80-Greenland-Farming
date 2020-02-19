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
YLABEL = "Frequency of Thaw-Freeze Events"
TITLE = "Frequency of Thaw-Freeze Events in Early Spring"
XBEGIN = 1955
XEND = 2020
XSTEP = 10
YBEGIN = 0
YEND = 10
YSTEP = 1
TIMES = "Times New Roman"
FONT = 12
FONT2 = 14
FIGNAME = "thawfreeze_paamiut.png"
TREND = "y = 0.002x + 0.378"
LAB_X = 0.2
LAB_Y1 = 0.8
LAB_Y2 = 0.75


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
    
    # graph aesthetics
    plt.xlabel(XLABEL, fontname = TIMES, fontsize = FONT)
    plt.ylabel(YLABEL, fontname = TIMES, fontsize = FONT)
    plt.xticks(np.arange(XBEGIN, XEND + 1, step = XSTEP), fontname = TIMES, fontsize = FONT)
    plt.yticks(np.arange(YBEGIN, YEND + 1, step = YSTEP), fontname = TIMES, fontsize = FONT)
    plt.title(TITLE, fontname = TIMES, fontsize = FONT2)
    
    # trendline
    z = np.polyfit(years, tfs, 1)
    p = np.poly1d(z)
    plt.plot(years, p(years),"b--")
    
    eq = TREND
    R = np.corrcoef(years, tfs)
    R2 = "R^2 = {}".format(round(R[0][1] ** 2, 4))
    
    plt.figtext(LAB_X, LAB_Y1, eq)
    plt.figtext(LAB_X, LAB_Y2, R2)
    
    plt.savefig(FIGNAME)
    


timeseries_image(fta.DATA)
