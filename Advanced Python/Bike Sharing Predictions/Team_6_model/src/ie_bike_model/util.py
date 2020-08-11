# coding: utf-8

# ### LOADING LIBRARIES

# In[1]:

import datetime as dt
import os
import pandas as pd


# #### File Directory

# In[3]:


def get_directory():
    library_dir = os.path.dirname(__file__)
    data_directory = os.path.join(library_dir, "data")
    return data_directory


# #### Data Reader

# In[4]:


def data_reader(hour_path=None):
    if hour_path is None:
        hour_path = os.path.join(get_directory(), "hour.csv")

    hour = pd.read_csv(hour_path, index_col="instant", parse_dates=True)
    return hour


# #### Model Path

# In[5]:


def get_model_path(model_dir=None, model="RandomForestRegressor"):
    if model_dir is None:
        model_dir = os.path.dirname(__file__)

    if model == "RandomForestRegressor":
        model_path = os.path.join(model_dir, "randomforest.pkl")

    return model_path


# #### Find Season

# Get season
def season(x):
    if x == 3 or x == 4 or x == 5:
        return 2
    if x == 6 or x == 7 or x == 8:
        return 3
    if x == 9 or x == 10 or x == 11:
        return 4
    if x == 12 or x == 1 or x == 2:
        return 1
