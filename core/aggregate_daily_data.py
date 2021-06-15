""" Functions to aggregate daily assessment data to monthly counts"""

import datetime as dt
import pandas as pd
pd.options.mode.chained_assignment = None


def clean_rows(df):
    """
    Remove na kick-off dates, remove duplicates
    :param df: pandas dataframe containing daily assessments
    :return: df with dropped rows
    """

    df = df[df['Assessment Kick-Off Date'].isna() == False]
    df.drop_duplicates(inplace=True, ignore_index=True)
    return df


def create_date_columns(df):
    """
    Create date columns (based on assessment kick off date)
    :param df: pandas dataframe containing daily assessments
    :return: df with additional date columns
    """

    df['Kick-Off_DATE'] = pd.to_datetime(df['Assessment Kick-Off Date'])
    df['kickoff_year_month'] = df['Kick-Off_DATE'].dt.strftime('%Y-%m')
    df['Year'] = df['Kick-Off_DATE'].dt.strftime('%Y')
    df['Month'] = df['Kick-Off_DATE'].dt.strftime('%m')
    df['Day'] = 1
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']]).dt.date
    return df


def one_hot_encode_assessment(df):
    """
    One hot encode assessment types, then sum cols (should be =1)
    Join back to daily df
    :param df: pandas dataframe containing daily assessments
    :return: df with additional assessment type cols
    """

    assessment_types = pd.get_dummies(df['Assessment Type'])
    assessment_types['total_assessments_computed'] = assessment_types.sum(axis=1)
    df = df.join(assessment_types)
    return df


def subset_data_by_schedule_status(df):
    """
    Subset to only rows where status is one of:
        Completed
        In Progress
        Scheduled

    :param df: pandas dataframe containing daily assessments
    :return: df with dropped rows
    """

    df = df[df['Assessment Schedule Status'].isin(
        ['Completed', 'In Progress', 'Scheduled'])]

    return df


def create_monthly_aggregate_from_daily_data(df):
    """
    Compute monthly assessment counts
    :param df: pandas dataframe containing daily assessments
    :return: dataframe where each row represents month
    """
    daily_restricted = df[['Date', 'ATT','LSCA','OA','SCA','TRA','total_assessments_computed']]
    monthly_data = daily_restricted.groupby('Date').sum()
    return monthly_data
#
#
#
#
# import os
# import datetime as dt
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import seaborn as sns
#
# df_daily = pd.read_csv(os.path.join('.', 'Assessment Data_Daily.csv'))
# print(f"shape daily data: {df_daily.shape}")
# df_daily = clean_rows(df_daily)
# print(f"shape daily data: {df_daily.shape}")
# df_daily = create_date_columns(df_daily)
# print(f"shape daily data: {df_daily.shape}")
# df_daily = one_hot_encode_assessment(df_daily)
# print(f"shape daily data: {df_daily.shape}")
# df_daily = subset_data_by_schedule_status(df_daily)
# print(f"shape daily data: {df_daily.shape}")
#
# df_daily.head()
#
# df_monthly = create_monthly_aggregate_from_daily_data(df_daily)
# df_monthly.tail(n=10)
# len(df_monthly )