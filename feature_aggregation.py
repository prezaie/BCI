#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:49:25 2019

@author: parisarezaie
"""

def feature_aggregation(input_data=conf.data.cleaned_data,
                        list_ops = conf.data.operating_states_static,
                        method = conf.data.method_of_aggregation):
    """Reduces whole features of DataFrame across all channels. Method function aggregates only over 
    vibration static operation features. For all other features, a regression line will be fitted.
    
    Args:
        input_data (str): expects a pkl file from the cleaned joined data set.
            (default: {conf.data.joined_data (from project config)})
        list_ops (list): list of vibration static operating states.  
            (default: {conf.data.operating_states_static(from project config)})  
        method (function): Aggregate function like mean, std or median for vibration static features
            (default: {conf.data.method_of_aggregation(from project config)})
    Returns:
        data (Dataframe): with reducted features
    """    
    data = pd.read_pickle(input_data).dropna(axis=1)
    channels = utils.get_channels(data)
    features = list(utils.get_all_features_from_channels(data, channels))
    vibration_static_features = list()
    hydraulic_vibration_features = list()
    for feature in features:
        if feature.split('#')[0] == "a_01X" and utils._get_wind(feature.rsplit('_', 1)[0]) in list_ops:
            vibration_static_features.append(feature)
        else:
            hydraulic_vibration_features.append(feature)          
    df_vibration_static_features = data.loc[:, vibration_static_features]
    df_hydraulic_vibration_features = data.loc[:, hydraulic_vibration_features]
    df_method = utils.apply_on_ops(df_vibration_static_features, list_ops, method)
    feat_list = list()
    for col in df_hydraulic_vibration_features.columns:
        feat = col.rsplit('_', 1)[0]
        feat_list.append(feat)
    df_new = pd.DataFrame()
    for f in list(set(feat_list)):
        df_param = feature_reduction.fit_windows_linear(df_hydraulic_vibration_features, f)
        df_new = pd.concat([df_new, df_param], axis=1)
    df_new.reset_index(drop=True, inplace=True)
    df_method.reset_index(drop=True, inplace=True)
    df_feature_reduction = pd.concat([df_new, df_method], axis=1)    
       
    return df_feature_reduction 