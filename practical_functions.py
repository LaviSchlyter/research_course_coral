# Import useful packages

import gdal
import pandas as pd
import geopandas as gpd
from io import StringIO
import osr
import matplotlib.pyplot as plt
import rtree
import pygeos
import os, json
from ipywidgets import widgets, IntSlider, jslink
import seaborn as sns
sns.set_theme(style="whitegrid")
import warnings
warnings.filterwarnings("ignore")

# Load image from local storage
from IPython.display import Image
from ipyleaflet import *



def mean_col(df, col_name):
    """
        df: dataframe
        col_name: list of columns 
        
        return:
        the mean values of the dataframe over the column of interest
    """
    return df[col_name].mean()

# 
def split_years(dt):
    """
        dt: dataframe
        return:
        Split the data frames based on the years
    """
    dt['year'] = dt['surveydate'].dt.year
    return [dt[dt['year'] == y] for y in dt['year'].unique()]


def make_geo_frame(df):
        """
        df: dataframe
        return:
        Geo-pandas dataframe 
    """
    return gpd.GeoDataFrame(df, geometry = 'geometry')


def export_shape(df, name):
        """
        df: geopandas dataframe
        name: string; name to give to the export file
        return:
        shape file with the given name string 
    """
    return df.to_file(name + '.shp', driver='ESRI Shapefile')

def trans_surv(df):
    """
        df: dataframe
        return
        list of zeros if no duplicate in the dataframe; else return the number of duplicates and the duplicate dataframe 
    """
    num = df.transectid.duplicated().sum()
    if (num):
        tran_id = df[df.transectid.duplicated()]["transectid"].item()
        return [num,df[df["transectid"] == tran_id]]
    else :
        return [0,0]
    
def smart_df(df, year):
    """
        df: dataframe 
        year: int
        return
        dataframe with the transectid (indentification of area) with year as a column filled with true
        // This function is used for efficient computing in the Notebook
    """
    df_ = df["transectid"]
    df_ = pd.DataFrame(df_)
    df_.set_index("transectid", inplace = True) 
    df_[year] = True
    return df_

# function to keep only columns of given list
def get_df_col(df, list_col):
    return df[list_col]

# Returns a list of indexes that correspond to the given condition
def get_index_list(df, cond):
    return df[df["Sum"] == cond].index.tolist()

# you return a dataframe given a list of indexes
def return_df(df, ind_list):
    return df.loc[ind_list]

def mean_region(df_s, df_joined, cond):
    """
        
    """
    df_s = df_s.set_index("transectid") 
    list_col = ["pr_hard_coral", "pr_soft_coral", "pr_algae", "pr_oth_invert", "pr_other", "geometry", "year"]
    df = get_df_col(df_s, list_col)
    return return_df(df, get_index_list(df_joined,  cond))

def plot_mean_stack(df, title):
    """
        Plot the df given the title as stacks histogram
    """

    # I will now group the pr_oth_invert and pr_other
    df["others"] = df["pr_oth_invert"] + df["pr_other"]
    df = df.drop(columns = ["pr_oth_invert", "pr_other"])

    # Here I make a specific dataframe to enable a stacked graph 
    #survey_melt = pd.melt(Survey_mean, id_vars = ["year"], value_vars=["pr_hard_coral", "pr_algae", "pr_soft_coral", "others"])
    survey_melt = pd.melt(df, id_vars = ["year"], value_vars=["pr_hard_coral", "pr_soft_coral","pr_algae","others"])
    fig, ax = plt.subplots(figsize=(10,7))  
    import numpy as np
    months = survey_melt['variable'].drop_duplicates()
    margin_bottom = np.zeros(len(survey_melt['year'].drop_duplicates()))
    colors = ["#005b96","#6497b1","#006D2C", "#31A354"]

    for num, month in enumerate(months):
        values = list(survey_melt[survey_melt['variable'] == month].loc[:, 'value'])

        survey_melt[survey_melt['variable'] == month].plot.bar(x='year',y='value', ax=ax, stacked=True, color = colors[num],
                                        bottom = margin_bottom, label=month)
        margin_bottom += values
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.ylabel("Proportion")
    plt.xlabel("Year")
    plt.title(title)
    plt.show()
    
def hard_algae_plot(df):
    """
        Plot the hard algea on a line plot as a function of the years
    """
    sns.set_style("darkgrid")
    sns.lineplot("year","pr_hard_coral", data = df, label = "Hard coral")
    sns.lineplot("year","pr_algae", data = df, label = "Algae")
    plt.ylabel("Proportion")
    plt.xlabel("Year")
    
def fun(df, list_12_17):
    """
        Given the indexes of surveys done both in 2012 and 2017; return a df with columns of interest (list_col)
    """
    list_col = ["pr_hard_coral", "pr_soft_coral", "pr_algae", "pr_oth_invert", "pr_other", "geometry", "year"]
    df = get_df_col(df.set_index("transectid"), list_col)
    return return_df(df, list_12_17)


def group_others(df):
    """
        Given a df; group columns of "proportion of other invertebrates and others" together in a new column named "others" 
    """
    df["others"] = df["pr_oth_invert"] + df["pr_other"]
    df = df.drop(columns = ["pr_oth_invert", "pr_other"])
    return df
    
