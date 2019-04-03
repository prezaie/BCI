#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:43:06 2019

@author: parisarezaie
"""

def drop_columns(data, drop_dict):
    """Drops specific columns from dataset

    Drops specific columns. Columns have been listed as values for the keys in the 
    given dictionary and returns a DataFrame. Dictionary keys are iot bits.

    Args:
        data (str, or DataFrame): input data
        drop_dict (dict) : dictionary of columns to be dropped. 

    Returns:
        data (Dataframe): cleaned data
    """
    
    List_of_columns = list()
    for key, value in drop_dict.items():
        List_of_columns.extend([i for i in value])
    data = data[data.columns.difference(List_of_columns)]
    
    return data