#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:47:39 2019

@author: parisarezaie
"""

def linear_fit(X, Y):
    """Calculate a linear regression for two sets of measurements

    Fits a regression line to two sets of measurements X and Y. X and Y should have same length. 

    Args:
        X (array_like): feature windows
        Y (array_like): one observation of data over its windows

    Returns:
        slope (float): slope of the regression line
        intercept (float): intercept of the regression line
        r_squared (float): coefficient of determination
    """

    slope, intercept, r_value, _, _ = stats.linregress(X, Y)
    r_squared = (r_value**2)

    return slope, intercept, r_squared