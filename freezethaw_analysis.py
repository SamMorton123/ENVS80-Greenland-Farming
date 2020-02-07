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


MONTH_LOC = 2
DAY_LOC = 3
YEAR_LOC = 4
TMAX_LOC = 5
TMAX_FLAG_LOC = 6
TMIN_LOC = 7
TMIN_FLAG_LOC = 8
TAVG_LOC = 9
UNACCEPTABLE_FLAGS = ['I']  # data flags that indicate unreliable data
DATA = 'data/paamiut_tempdata2.xlsx'
JANUARY = 1
AUGUST = 8
MONTH = 30
FREEZING_TEMP = 0
THAW_FREEZE_INTERVAL = 40
FIRST_YEAR = 1958
FINAL_YEAR = 2018


def open_df(filename):
    '''
    Open Excel data as a pandas DataFrame. Return the DataFrame.
    '''
    
    df = pd.read_excel(filename)
    return df


def data_check(df, idx):
    '''
    Verify if a data row is valid. Data is invalid either if there is missing
    data or if the temperature flags are present in the list of unacceptable 
    flags. Returns True if the data row is valid, False otherwise.
    df - the DataFrame
    idx - the index of the row to be checked
    '''
    
    # verify that the data isn't missing
    if pd.isna(df.iloc[idx, TMAX_LOC]) or pd.isna(df.iloc[idx, TMIN_LOC]):
        return False
    
    # verify that the temperature flags are acceptable
    tmax_flags = df.iloc[idx, TMAX_FLAG_LOC]
    tmin_flags = df.iloc[idx, TMIN_FLAG_LOC]
    
    if len(tmax_flags) == 0 or len(tmin_flags) == 0:
        return False
    
    for i in range(len(tmax_flags)):
        if tmax_flags[i] in UNACCEPTABLE_FLAGS:
            return False
    
    # check each flags separately because they may be different lengths
    for i in range(len(tmin_flags)):
        if tmin_flags[i] in UNACCEPTABLE_FLAGS:
            return False
    
    return True


def locate_year_beginning(df, year, start_idx):
    '''
    Locate the df index of the start of a given year. Return None if the start_idx
    is beyond the first month of the given year
    df - the DataFrame
    year - the year you want the spring estimate for
    start_idx - the given starting index
    '''
    
    # check if the start idx is None
    if start_idx is None:
        return None
    
    # check that the start_idx doesn't put you beyond the year
    if df.iloc[start_idx, YEAR_LOC] > year or (df.iloc[start_idx, YEAR_LOC] == year and df.iloc[start_idx, MONTH_LOC] > JANUARY):
        return None
    
    # get a list of the indicies in the df
    indicies = list(df.index)
    
    # loop through the df rows until you find January of the given year
    for i in range(start_idx, len(indicies)):
        if df.iloc[i, YEAR_LOC] == year and df.iloc[i, MONTH_LOC] == JANUARY:
            return i
    
    return None


def estimate_spring_date(df, temp_metric, year, start_idx = 0):
    '''
    Estimate the date of "Spring," or the date in which temperatures stay above
    freezing for the rest of the growing season. The method assumes that freezing
    temperatures won't happen once August begins, and that if there hasn't been
    freezing temperatures for a month, then Spring began on that first non-freezing
    day. Returns the df index of the day in question.
    df - the DataFrame
    temp_metric - the way in which temperature will be assessed; the data has
    temp max, temp min, and temp avg.
    year - the year you want the spring estimate for
    start_index - specify a starting index for the method to cut down on iteration
    time
    '''
    
    # locate the beginning index of the given year; return None if the starting index is beyond the specified year
    year_idx = locate_year_beginning(df, year, start_idx)
    
    # if year_idx is None, return None
    if year_idx is None:
        return None
    
    # init track for spring beginning
    spring = year_idx 
    
    while True:
        
        # if it's been a month since the last below freezing day end the loop
        if year_idx - spring >= MONTH:
            return year_idx - MONTH
        
        if df.iloc[year_idx, temp_metric] < FREEZING_TEMP:
            spring = year_idx + 1
        
        year_idx += 1
    
    return year_idx


def thaw_freeze(df, idx, temp_metric):
    '''
    Check if there is a "thaw-freeze" event at the given index. A "thaw-freeze"
    event is when a day in which the average temp is above freezing is followed
    by a day in which the average temp is below freezing.
    df - the DataFrame
    idx - idx of the day in the data to check
    temp_metric - the way in which temperature will be assessed; the data has
    temp max, temp min, and temp avg.
    '''
    
    # if the given day has a temp above freezing
    if df.iloc[idx, temp_metric] > FREEZING_TEMP:
        
        # if the following day is then below freezing
        if df.iloc[idx + 1, temp_metric] <= FREEZING_TEMP:
            return True
        
        # if the following day is then above freezing
        else:
            return False
    
    # if the given day is below freezing then there is no thaw-freeze event
    else:
        return False


def calc_thaw_freeze(df, year_idx):
    '''
    Calculate the number of thaw-freeze events in the time leading up to a given
    date
    '''
    
    # check year_idx
    if year_idx is None:
        return -1
    
    # init counter of thaw-freeze events
    count = 0
    for i in range(year_idx - THAW_FREEZE_INTERVAL, year_idx - 1):
        if thaw_freeze(df, i, TAVG_LOC):
            count += 1
    
    return count


def generate_thaw_freeze_data(df, start = 0):
    '''
    Go through each year in the data and calculate how many thaw-freeze events
    there are. Optional parameter allows you to specify which date to start at.
    Assumes that each year should have enough data except 2019-2020.
    df - the DataFrame
    start - optional start index parameter
    '''
    
    # init list to hold the data
    data = []
    
    # init curr_idx at start
    curr_idx = start
    
    # loop through each year
    for year in range(FIRST_YEAR, FINAL_YEAR + 1):
        
        try_date = estimate_spring_date(df, TAVG_LOC, year, start_idx = curr_idx)
        if try_date is not None:
            curr_idx = try_date
        
            # calc the number of thaw-freeze events for that year
            thaw_freeze = calc_thaw_freeze(df, curr_idx)
        
            # add to the list of data
            data.append(thaw_freeze)
        
        # add -1 to the dataset to indicate unavailable datsa
        else:
            data.append(-1)
        
        
        '''
        # estimate the spring date for that year
        curr_idx = estimate_spring_date(df, TAVG_LOC, year, start_idx = curr_idx)
        
        # calc the number of thaw-freeze events for that year
        thaw_freeze = calc_thaw_freeze(df, curr_idx)
        
        # add to the list of data
        data.append(thaw_freeze)
        '''
    
    return data
        

# === Main Function ===
df = open_df(DATA)
data = generate_thaw_freeze_data(df)
print(data)







