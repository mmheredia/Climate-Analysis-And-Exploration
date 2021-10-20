
# Imports

from os import name
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.dates as mdates
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Flask Setup

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepapre(engine, reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

# List all of the routes available

@app.route("/")
def home():
    """List available API routes"""
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation route

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    max_date = dt.date(2017, 8, 23)
    previous_year = max_date - dt.timedelta(days = 365)

    past_year = (session.query(measurement.date, measurement.prcp).\
        filter(measurement.date <= max_date).\
            filter(measurement.date >= previous_year).\
                order_by(measurement.date).all())

    session.close()

    precipitation = {date: prcp for date, prcp in past_year}

    return jsonify(precipitation)

# Stations route

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    
    all_stations = session.query(station.station, station.name).all()

    session.close()
    
    return jsonify(all_stations)

# Tobs route

@app.route('/api/v1.0/tobs') 
def tobs():  

    session = Session(engine)

    max_date = dt.date(2017, 8 ,23)
    previous_year = max_date - dt.timedelta(days = 365)

    session.close()

    last_year = (session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
            filter(measurement.date <= max_date).\
                filter(measurement.date >= previous_year).\
                    order_by(measurement.tobs).all())
    
    return jsonify(last_year)

# Start route

@app.route("/api/v1.0/<start>")
def start(start = None):

    session = Session(engine)

    no_end = (session.query(measurement.tobs).\
        filter(measurement.date.between(start, '2017-08-23')).all())
    
    session.close()

    no_end_df = pd.DataFrame(no_end)

    tmin = no_end_df["tobs"].min()
    tavg = no_end_df["tobs"].mean()
    tmax = no_end_df["tobs"].max()
    
    return jsonify(tmin, tavg, tmax)

# Start and end route

def trstartendip1(start = None, end = None):

    session = Session(engine)

    end = (session.query(measurement.tobs).\
        filter(measurement.date.between(start, end)).all())
    
    session.close()

    end_df = pd.DataFrame(end)

    tmin = end_df["tobs"].min()
    tavg = end_df["tobs"].mean()
    tmax = end_df["tobs"].max()
    
    return jsonify(tmin, tavg, tmax)

if __name__ == "__main__":
    app.run(debug = True)