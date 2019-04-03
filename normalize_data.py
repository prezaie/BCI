#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:45:23 2019

@author: parisarezaie
"""

def normalize_data(input_data, window_size):
    """Normalizes data from dataset

    Normalizes data using rolling median and rolling standard deviation with
    certain window size. Function normalizes measurement columns and returns
    a normalized DataFrame

    Args:
        input_data (str, or DataFrame): input data
        window_size (int) :size of window for rolling median and standard deviation calculation

    Returns:
        normalized_data (Dataframe): normalized data
    """

    df = read_file(input_data)
    df['TStart'] = df['TStart'].astype('datetime64[ns]')
    df = df.sort_values(by='TStart')
    df = df.reset_index(drop=True)
    measurement_cols = utils.get_measurements(df)
    measurement_data = df[measurement_cols]
    measurement_data = pd.concat([measurement_data, df['TrueOK']], axis=1)
    measurement_data.loc[:, "TrueOK"] = measurement_data.loc[:, "TrueOK"].apply(
        lambda x: 1 if x == 'NOk' else 0)
    measurement_data.loc[:, measurement_data.select_dtypes(include=['object']).columns] =\
        measurement_data.loc[:, measurement_data.select_dtypes(
            include=['object']).columns].astype('float')

    def rolling_median(df):
        return df.rolling(window=window_size, axis=0, center=True, min_periods=1).median()

    def rolling_std(df):
        return df.rolling(window=window_size, axis=0, center=True, min_periods=1).std()

    df_rolling_median = measurement_data.groupby('TrueOK').apply(rolling_median)
    df_rolling_median.loc[df_rolling_median[df_rolling_median['TrueOK'] == 1].index,
                          df_rolling_median.columns != 'TrueOK'] = np.NaN
    df_rolling_std = measurement_data.groupby('TrueOK').apply(rolling_std)
    # rolling std function from Panda was incorrectly rewriting over all TrueOK columns and was
    # changing all of them to 1; we had to read the original one fram measurement_data DataFrame
    df_rolling_std.loc[:, "TrueOK"] = measurement_data["TrueOK"]
    df_rolling_std.loc[df_rolling_std[df_rolling_std['TrueOK'] == 1].index,
                       df_rolling_std.columns != 'TrueOK'] = np.NaN
    df_rolling_median.fillna(method='ffill', inplace=True)
    df_rolling_std.fillna(method='ffill', inplace=True)
    df_rolling_median = df_rolling_median[df_rolling_median.columns.drop(['TrueOK'])]
    df_rolling_std = df_rolling_std[df_rolling_std.columns.drop(['TrueOK'])]
    df[measurement_cols] = (df[measurement_cols] - df_rolling_median) / df_rolling_std

    return df
