import pandas as pd
import numpy as np
import datetime as data

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of date and precipitation"""
    # Query precipiation data
    precipitation = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert to dictionary using date ad the key and prcp as the value
    for u in precipitation:
        print(u._asdict())
    # measurements_data = []
    # for date, prcp in precipitation:
    #     measurements_dict = {}
    #     measurments_dict["date"] = date
    #     measurements_dict["prcp"] = prcp
    #     measurments_data.append(measurements_dict)


    # Return JSON representation1
    return jsonify(precipitation)



if __name__ == '__main__':
    app.run(debug=True)
