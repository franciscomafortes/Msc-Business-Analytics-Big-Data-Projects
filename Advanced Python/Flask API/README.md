# Bike sharing Prediction Model by Francisco Fortes

## Overview of Project

The `app.py` contains code for the flask application. The rest of the files refer to the `ie_bike_model` package from the group assignment.

## Running the Web application

1. Install  `ie_bike_model` package:  

```
$ pip install .
```
2. Let's make sure that we have  `flask` installed, otherwise:
```
$ pip install flask
```

3. In order to run the app, let's type in the command line:

```
$ flask run
```

## Obtaining the prediction

Then open [this sample link](http://127.0.0.1:5000/predict?date=2012-01-01T00:00:00&weathersit=1&temperature_C=9.84&feeling_temperature_C=14.395&humidity=81.0&windspeed=0)
in your browser.

On this page user can see the model (Ridge or XGBoost by default) that the predictions were made with, prediction of the number of bikes and RMSE score.

The code for this ie-bike-model was used from Professor Juan, source:[github link](https://github.com/IE-Advanced-Python/ie-bike-sharing-model-lib-ref)
