import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.Measurements
Stations = Base.classes.Stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f" /api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/stations")
def names():
    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Stations.name).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of dates and temperature observations from the last year"""
    # Query all passengers
    prev_year = dt.date.today() - dt.timedelta(days=365)

    #date_str = "2017"
    results=session.query(Measurements.date,Measurements.prcp).\
    filter(Measurements.date >= prev_year).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    measure = []
    for measure in results:
        measure_dict = {}
        measure_dict["date"] = measure.date
        measure_dict["prcp"] = measure.prcp
        measure.append(measure_dict)

    return jsonify(measure)

@app.route("/api/v1.0/tobs")
def temperature():
    """Return a list of dates and temperature observations from the last year"""
    # Query all passengers
    prev_year = dt.date.today() - dt.timedelta(days=365)

    #date_str = "2017"
    results=session.query(Measurements.tobs).\
    filter(Measurements.date >= prev_year).all()
    all_names = list(np.ravel(results))
    return jsonify(all_names)


if __name__ == '__main__':
    app.run(debug=True)
