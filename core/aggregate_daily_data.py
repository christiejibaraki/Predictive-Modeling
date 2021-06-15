""" Functions to aggregate daily assessment data to monthly counts"""

import pandas as pd
pd.options.mode.chained_assignment = None


def clean_rows_helper(df):
    """
    Remove na kick-off dates, remove duplicates
    :param df: pandas dataframe containing daily assessments
    :return: df with dropped rows
    """

    df = df[df['Assessment Kick-Off Date'].isna() == False]
    df.drop_duplicates(inplace=True, ignore_index=True)
    return df


def create_date_columns_helper(df):
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


def one_hot_encode_assessment_helper(df):
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


def subset_data_by_schedule_status_helper(df):
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


def create_monthly_aggregate_from_daily_data_helper(df):
    """
    Compute monthly assessment counts helper
    :param df: pandas dataframe containing daily assessments
    :return: dataframe where each row represents month
    """
    daily_restricted = df[['Date', 'ATT','LSCA','OA','SCA','TRA','total_assessments_computed']]
    monthly_data = daily_restricted.groupby('Date').sum()
    return monthly_data


def compute_monthly_assessment_counts(df):
    """
    Compute monthly assessment counts
    :param df: unprocessed pandas dataframe containing daily assessments
    :return: dataframe of monthly assessment ct data
    """

    df = clean_rows_helper(df)
    df = create_date_columns_helper(df)
    df = one_hot_encode_assessment_helper(df)
    df = subset_data_by_schedule_status_helper(df)
    return create_monthly_aggregate_from_daily_data_helper(df)
