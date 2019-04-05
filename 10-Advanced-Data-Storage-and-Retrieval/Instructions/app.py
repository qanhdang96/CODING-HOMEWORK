# Import Dependencies
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def homepage():
    """List all routes that are available."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"List of precipitation from last year from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"List of stations from the dataset<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"List of Temperature Observations (tobs) for the previous year<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"List of the minimum temperature, the average temperature, and the max temperature for a given start<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"List of the minimum temperature, the average temperature, and the max temperature for a given start-end range<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """List of precipitation from last year from all stations:"""
    recent_date = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > last_year).\
    order_by(Measurement.date).all()
    precipitation_data = dict(precipitation)
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def station():
    """List of stations from the dataset:"""
    active = session.query(Measurement.station).\
    group_by(Measurement.station).all()
    stations_data= list(np.ravel(active))
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    """List of Temperature Observations (tobs) for the previous year:"""
    recent_date = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > last_year).\
    order_by(Measurement.date).all()

    tobs_result = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_year).all()
    tobs_data = list(tobs_result)
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def daily_normals(start):
    """List of the minimum temperature, the average temperature, and the max temperature for a given start:"""
    start_trip = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    start_data=list(start_trip)
    return jsonify(start_data)

@app.route("/api/v1.0/<start>/<end>")
def my_trip(start,end):
    """List of the minimum temperature, the average temperature, and the max temperature for a given start-end range:"""
    trips_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    trips_data=list(trips_dates)
    return jsonify(trips_data)

if __name__ == "__main__":
    app.run(debug=True)