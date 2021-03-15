import pandas as pd
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


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
        f"Available Hawaii API Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# -------------------
# precipitation route
# -------------------
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of date and precipitation"""
    # Query precipiation data
    current_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Slice the data and convert to integers
    current_date[0][0:4]
    current_year = int(current_date[0][0:4])
    current_month = int(current_date[0][5:7])
    current_day = int(current_date[0][8:])

    # Pass the integers to find the year of data
    query_enddate = dt.date(current_year, current_month, current_day) - dt.timedelta(days=365)

    query_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_enddate).all()
    
    session.close()

    # Convert to dictionary using date ad the key and prcp as the value
    all_query = []
    for date, prcp in query_data:
        query_dict = {}
        query_dict["date"] = date
        query_dict["prcp"] = prcp
        all_query.append(query_dict)

    # Return JSON representation1
    return jsonify(all_query)


# -------------------
# stations route
# -------------------
@app.route("/api/v1.0/stations")
def stations():

    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations"""
    # Query station data

    stations = session.query(Measurement.station, func.count(Measurement.station))\
    .group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    # Return JSON representation1
    return jsonify(stations)


# -------------------
# tobs route -- HOW TO DEFINE THE START DATE AS A VARIABLE, SAME PROBLEM IN THE JUPYTER NOTEBOOK
# -------------------
@app.route("/api/v1.0/tobs")
def tobs():

    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of temperature observations for the previous year"""
    # Get last year
    # query_enddate = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Change getting the year to passing variables
    current_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Slice the data and convert to integers
    current_year = int(current_date[0][0:4])
    current_month = int(current_date[0][5:7])
    current_day = int(current_date[0][8:])

    # Pass the integers to find the year of data
    query_enddate = dt.date(current_year, current_month, current_day) - dt.timedelta(days=365)

    # Query station data
    most_active = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc()).first()

    query_data2 = session.query(Measurement.date, Measurement.station, Measurement.tobs )\
    .filter(Measurement.station == most_active[0]).filter(Measurement.date >= query_enddate).all()
    
    session.close()

    # Convert list of tuples into normal list
    # class 10-advanced-data-storage, 10-Ins_Flask_with_ORM
    query_list2 = list(np.ravel(query_data2))


    # Return JSON representation1
    return jsonify(query_list2)


# -------------------
# start date route -- INCOMPLETE, NEED TO DEFINE THE START DATE 
# -------------------
@app.route("/api/v1.0/<start>")
def filter_start(start):

    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, max temperature from the start"""
    # Query station data

    query_data3 = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start).all()
    
    session.close()

    # Convert list of tuples into normal list
    # class 10-advanced-data-storage, 10-Ins_Flask_with_ORM
    query_list3 = list(np.ravel(query_data3))
    
    # Return JSON representation1
    return jsonify(query_list3)


# -------------------
# start_end date route -- INCOMPLETE, NEED TO DEFINE THE START AND END DATES
# -------------------
@app.route("/api/v1.0/<start>/<end>")
def filter(start, end):

    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, max temperature from the start"""
    # Query station data

    query_data4 = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs))\
    .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    # Convert list of tuples into normal list
    # class 10-advanced-data-storage, 10-Ins_Flask_with_ORM
    query_list4 = list(np.ravel(query_data4))
    
    # Return JSON representation1
    return jsonify(query_list4)



if __name__ == '__main__':
    app.run(debug=True)
