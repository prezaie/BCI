#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 21:41:01 2019

@author: parisarezaie
"""

def remove_duplicate(input_data, logpath=None):
    """Removes duplicate from dataset

    Drops all rows that have duplicates. Pumps that have exact measure data
    but different serial number.Function drop duplicates and return a cleaned DataFrame

    Args:
        input_data (str, or DataFrame): input data
        logpath (str): (optional) path where dataframes store.(default: {None})

    Returns:
        measurement_data_clean (Dataframe): clean data
    """

    df = read_file(input_data)
    measurement_cols = utils.get_measurements(df)
    measurement_data = df[measurement_cols]
    duplicates_index = measurement_data.duplicated()
    measurement_data_duplicates = measurement_data[duplicates_index]
    measurement_data_clean = df[~duplicates_index]
    # write dropped rows to excel file
    if logpath is not None:
        dupe_data = \
            measurement_data_duplicates.loc[:, list(map(lambda col: col not in measurement_cols,
                                               measurement_data_duplicates.columns))]
        logfile = os.path.join(logpath, f"cleaning_duplicate_rows_v{conf.data.version}.xlsx")
        print("=== cleaning.reduction_duplicate ---")
        print("=== rows that are dropped due to duplicate values written to file:")
        print("=== {}".format(logfile))
        dupe_data.to_excel(logfile)
    else:
        print("=== cleaning.reduction_duplicate ---")
        print("=== removed rows due to duplicate values:")
        print(measurement_data_duplicates)

    return measurement_data_clean