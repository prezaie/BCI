#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:48:20 2019

@author: parisarezaie
"""

def fit_windows_linear(data, feature_name):
    """ Reduces features by fitting a linear line

    Reduces  features. Fits a linear function to several operating states windows' and 
    obtains new featuers

    Args:
        data (DataFrame): DataFrame of vibration non_static operating states and hydraulic static
        and non_static operating states
        feature_name (string) : name of operating state feature.Feature name is currently
        "nan#avg_iot18_windXY". However this doesn't work. You need to pass "nan#avg_iot18" instead 

    Returns:
        data (Dataframe): with three columns: Slope, intercept and r_squared(
        coefficient of determination) of fitted line
    """

    
    df = data.loc[:, utils.get_measurements(data, feature_name)]
    df.columns = df.columns.to_series().apply(utils._get_wind)
    df = df[sorted(df.columns.tolist())]
    df_col_val = df.columns.values
    df_param = pd.DataFrame()
    vals = list(df.apply(lambda row: list(fitting.linear_fit(
        df_col_val, np.array(row).reshape(df_col_val.shape[0],))), axis=1))
    df_param = pd.DataFrame(np.concatenate(vals).reshape(len(vals), 3),
                            columns=[f"{feature_name}_slope", f"{feature_name}_intercept", f"{feature_name}_r2"])

    return df_param