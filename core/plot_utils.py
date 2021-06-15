"""Plotting functions"""
import matplotlib.pyplot as plt
import seaborn as sns


def create_count_data(df, group):
    """
    create dataframe of counts based on groupby
    :param df: pandas dataframe
    :param group: name of column to groupby
    :return: dataframe of counts for each group
    """
    counts = df.groupby(group).size().to_frame('count')
    counts.reset_index(inplace=True)
    return counts


def create_barplot(count_data, grouped_by_col, count_col, title):
    """
    create bar plot based on grouped_by_col
    """
    plt.figure(figsize=(20,6))
    p = sns.barplot(x=grouped_by_col, y=count_col,
                data=count_data)
    p.set_xticklabels(p.get_xticklabels(), rotation=40, ha="right")
    plt.ylabel("Count", size=15)
    plt.xlabel(grouped_by_col, size=15)
    plt.title(title, size=18)
    plt.show()
