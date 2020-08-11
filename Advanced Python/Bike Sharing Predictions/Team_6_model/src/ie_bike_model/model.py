# coding: utf-8

# ### Loading Libraries

# In[2]:

import datetime as dt
import os
from pathlib import Path
import re

import joblib
import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from scipy.stats import skew
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from ie_bike_model.util import data_reader, get_model_path, season


US_HOLIDAYS = calendar().holidays()


# ### Feature engineering

# In[3]:


def feat_engineering(hour):
    hour = hour.copy()

    # Rented during office hours
    hour["IsOfficeHour"] = np.where(
        (hour["hr2"] >= 9) & (hour["hr2"] < 17) & (hour["weekday2"] == 1), 1, 0
    )
    hour["IsOfficeHour"] = hour["IsOfficeHour"].astype("category")

    # Rented during daytime
    hour["IsDaytime"] = np.where((hour["hr2"] >= 6) & (hour["hr2"] < 22), 1, 0)
    hour["IsDaytime"] = hour["IsDaytime"].astype("category")

    # Rented during morning rush hour
    hour["IsRushHourMorning"] = np.where(
        (hour["hr2"] >= 6) & (hour["hr2"] < 10) & (hour["weekday2"] == 1), 1, 0
    )
    hour["IsRushHourMorning"] = hour["IsRushHourMorning"].astype("category")

    # Rented during evening rush hour
    hour["IsRushHourEvening"] = np.where(
        (hour["hr2"] >= 15) & (hour["hr2"] < 19) & (hour["weekday2"] == 1), 1, 0
    )
    hour["IsRushHourEvening"] = hour["IsRushHourEvening"].astype("category")

    # Rented during most busy season
    hour["IsHighSeason"] = np.where((hour["season2"] == 3), 1, 0)
    hour["IsHighSeason"] = hour["IsHighSeason"].astype("category")

    # binning temp, atemp, hum in 5 equally sized bins
    bins = [0, 0.19, 0.49, 0.69, 0.89, 1]
    hour["temp_binned"] = pd.cut(hour["temp2"], bins).astype("category")
    hour["hum_binned"] = pd.cut(hour["hum2"], bins).astype("category")

    return hour


# ### Pre-processing

# In[4]:


def preprocessing(hour):

    hour = hour.copy()

    # creating duplicate columns for feature engineering
    hour["hr2"] = hour["hr"]
    hour["season2"] = hour["season"]
    hour["temp2"] = hour["temp"]
    hour["hum2"] = hour["hum"]
    hour["weekday2"] = hour["weekday"]

    # Change dteday to date time
    hour["dteday"] = pd.to_datetime(hour["dteday"])

    # Convert the data type to eithwe category or to float
    int_hour = [
        "season",
        "yr",
        "mnth",
        "hr",
        "holiday",
        "weekday",
        "workingday",
        "weathersit",
    ]
    for col in int_hour:
        hour[col] = hour[col].astype("category")

    # Log of the count since log0 is invalid so we use log1p.
    logws = round(skew(np.log1p(hour.windspeed)), 4)
    # Sqrt of the count
    sqrtws = round(skew(np.sqrt(hour.windspeed)), 4)
    hour["windspeed"] = np.log1p(hour.windspeed)

    # Log of the count
    logcnt = round(skew(np.log(hour.cnt)), 4)
    # Sqrt of the count
    sqrtcnt = round(skew(np.sqrt(hour.cnt)), 4)
    hour["cnt"] = np.sqrt(hour.cnt)

    hour = feat_engineering(hour)

    # dropping duplicated rows used for feature engineering
    hour = hour.drop(columns=["hr2", "season2", "temp2", "hum2", "weekday2"])

    return hour


# ### Dummifying Variables

# In[5]:


def dummify(hour, known_columns=None):

    hour = pd.get_dummies(hour)
    if known_columns is not None:
        for col in known_columns:
            if col not in hour.columns:
                hour[col] = 0

        hour = hour[known_columns]

    return hour


# ### Modelling

# #### Split Train & Test

# In[8]:


def split_train_test(hour):

    hour = hour.copy()

    # Split into train and test
    hour_train, hour_test = hour.iloc[0:15211], hour.iloc[15212:17379]
    train = hour_train.drop(columns=["dteday", "casual", "atemp", "registered"])
    test = hour_test.drop(columns=["dteday", "casual", "registered", "atemp"])

    # seperate the independent and target variable on training data
    train_X = train.drop(columns=["cnt"], axis=1)
    train_y = train["cnt"]

    # seperate the independent and target variable on test data
    test_X = test.drop(columns=["cnt"], axis=1)
    test_y = test["cnt"]

    return train_X, test_X, train_y, test_y


# #### Random Forest

# In[ ]:


def train_rf(hour):

    hour = hour.copy()

    hour_d = pd.get_dummies(hour)
    regex = re.compile(r"\[|\]|<", re.IGNORECASE)
    hour_d.columns = [
        regex.sub("_", col) if any(x in str(col) for x in set(("[", "]", "<"))) else col
        for col in hour_d.columns.values
    ]

    hour_d = hour_d.select_dtypes(exclude="category")

    hour_d_train_x, hour_d_test_x, hour_d_train_y, hour_d_test_y = split_train_test(
        hour_d
    )

    rf = RandomForestRegressor(
        max_depth=40,
        min_samples_leaf=1,
        min_samples_split=2,
        n_estimators=200,
        random_state=42,
    )

    rf.fit(hour_d_train_x, hour_d_train_y)

    return rf


# ### Post-Processing

# In[ ]:


def postprocessing(hour):

    hour = hour.copy()
    hour.columns = hour.columns.str.replace("[\[\]\<]", "_")

    return hour


# ### Train and Persist

# In[11]:


def train_and_persist(model_dir=None, hour_path=None, model="RandomForestRegressor"):

    hour = data_reader(hour_path)
    hour = preprocessing(hour)
    hour = dummify(hour)
    hour = postprocessing(hour)

    if model == "RandomForestRegressor":
        model_clf = train_rf(hour)

    model_path = get_model_path(model_dir, model)
    joblib.dump(model_clf, model_path)


# ### Input Paramaters as Dictionary

# In[ ]:


def get_input_dict(parameters):

    hour_original = data_reader()
    base_year = pd.to_datetime(hour_original["dteday"]).min().year

    date = parameters["date"]
    parameters["dteday"] = parameters.pop("date")

    is_holiday = date in US_HOLIDAYS
    is_weekend = date.weekday() in (5, 6)

    row = pd.Series(
        {
            "dteday": parameters["dteday"].strftime("%Y-%m-%d"),
            "season": season(parameters["dteday"].month),
            "yr": parameters["dteday"].year,
            "mnth": parameters["dteday"].month,
            "hr": parameters["dteday"].hour,
            "holiday": 1 if is_holiday else 0,
            "weekday": parameters["dteday"].weekday() + 1,
            "workingday": 0 if is_holiday or is_weekend else 1,
            "weathersit": parameters["weathersit"],
            "temp": parameters["temperature_C"] / 41.0,
            "atemp": parameters["feeling_temperature_C"] / 50.0,
            "hum": parameters["humidity"] / 100.0,
            "windspeed": np.log1p(parameters["windspeed"] / 67),
            "cnt": np.sqrt(1),  # Dummy, unused for prediction
        }
    )

    dummified_original = dummify(preprocessing(hour_original))

    df = pd.DataFrame([row])
    df = preprocessing(df)
    df = dummify(df, dummified_original.columns)
    df = postprocessing(df)

    df = df.drop(columns=["dteday", "atemp", "casual", "registered", "cnt"])

    assert len(df) == 1

    return df.iloc[0].to_dict()


# ### Predict

# In[12]:


def predict(parameters, model_dir=None, model_name="RandomForestRegressor"):

    model_path = get_model_path(model_dir, model=model_name)
    print(model_path)
    if not os.path.exists(model_path):
        train_and_persist(model_dir, model=model_name)

    model_clf = joblib.load(model_path)

    input_dict = get_input_dict(parameters)
    X_input = pd.DataFrame([pd.Series(input_dict)])

    result = model_clf.predict(X_input)

    # Undo np.sqrt(hour["cnt"])
    return int(result ** 2)


# ### Obtaining Score

# In[13]:


def score(model_dir=None, hour_path=None, model_name="RandomForestRegressor"):
    model_path = get_model_path(model_dir, model=model_name)
    if not os.path.exists(model_path):
        train_and_persist(model_dir, model=model_name)

    model_clf = joblib.load(model_path)

    hour = data_reader(hour_path)
    hour = preprocessing(hour)
    hour = dummify(hour)
    hour = postprocessing(hour)

    hour_d = pd.get_dummies(hour)
    regex = re.compile(r"\[|\]|<", re.IGNORECASE)
    hour_d.columns = [
        regex.sub("_", col) if any(x in str(col) for x in set(("[", "]", "<"))) else col
        for col in hour_d.columns.values
    ]

    hour_d = hour_d.select_dtypes(exclude="category")

    hour_d_train_x, hour_d_test_x, hour_d_train_y, hour_d_test_y = split_train_test(
        hour_d
    )

    r2_train = model_clf.score(hour_d_train_x, hour_d_train_y)
    r2_test = model_clf.score(hour_d_test_x, hour_d_test_y)
    return r2_train, r2_test
