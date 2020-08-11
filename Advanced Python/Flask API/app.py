import argparse
import sys
import time

import datetime as dt

import sklearn
from flask import Flask
from flask import request

from lib import ie_bike_model
from lib.ie_bike_model.model import train_and_persist, predict

app = Flask(__name__)

#1)
@app.route("/")
def versions():

    x = {
        "sklearn_V": sklearn.__version__,
        "ie_bike_model_V": ie_bike_model.__version__,
        "Python_V": sys.version[:5],
    }
    return x
#2)
@app.route("/train_and_persist", methods=["POST"])
def train_and_persist_endpoint():

    _ = train_and_persist()
    return {"status": "ok"}

#3)
@app.route("/predict")
def predict_endpoint():

    start_time = time.time()

    request_args = request.args

    parameters = {}

    try:
        date_str = request_args["date"]
    except KeyError:
        return {"error_message": "`date` argument is missing"}, 400

    try:
        date = dt.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return (
            {
                "error_message": "`date` argument must be in the form `%Y-%m-%dT%H:%M:%S`"
            },
            400,
        )
    else:
        parameters["date"] = date

    try:
        weathersit = request_args["weathersit"]
    except KeyError:
        return {"error_message": "`weathersit` argument is required"}, 400
    else:
        parameters["weathersit"] = weathersit

    float_params = ["temperature_C", "feeling_temperature_C", "humidity", "windspeed"]

    for param in float_params:
        try:
            param_value = request_args[param]
        except KeyError:
            return {"error_message": "`{}` argument is required".format(param)}, 400

        try:
            param_value = float(param_value)
        except ValueError:
            return (
                {"error_message": "Value of `{}` must be a number".format(param)},
                400,
            )

        parameters[param] = param_value

    num_of_cyclists = predict(parameters)

    elapsed_time = round(time.time() - start_time, 3)

    response = {"result": num_of_cyclists, "elapsed_time": elapsed_time}
    return response

#Debugger
def parse_args():

    parser = argparse.ArgumentParser("Flask App")

    parser.add_argument("--debug", dest="debug", action="store_true", default=False)

    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":

    arguments = parse_args()
    debug = arguments.debug

    app.run(debug=debug)
