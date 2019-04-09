#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 12:17:42 2019

@author: parisarezaie
"""

def apply_on_ops(df, list_ops, method):
    """Aggregates over all window columns for operating states

    Uses method that has been given for aggregation over all window columns of a operating state. 
    Function returns a dataframe of aggregated features.

    Args:
        df (DataFrame): DataFrame 
        list_ops (list): list of operating states
        method (function): aggregate function like mean, std or median

    Returns:
        df_method (Dataframe): aggregated data
    """
    

    def cal_windows_agg(df, key, method):
        wins = get_all_windows_from_feature(df, key)
        df_agg = pd.DataFrame()
        df_agg.loc[:, key + '_' + method] = df.loc[:, wins].agg(method, axis=1)
        return df_agg

    feature_list = list()
    for i in list_ops:
        feature_list.extend(get_measurements(df, 'iot' + str(i)))

    df_features = df[feature_list]
    keys = list(set(map(lambda col: col.rsplit("_", 1)[0], feature_list)))
    df_method = pd.concat(
        map(lambda key: cal_windows_agg(df_features, key, method), keys), axis=1)

    return df_method
