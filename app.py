import numpy as np 
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#keeping with convention

meas = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

# Routes

@app.route("/")
def welcome():
    
    return (
        f"Hello There<br/>"
        f"Here are our api routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    """Return a list of all Precipitation Data"""
    results = session.query(meas.date, meas.prcp).\
        filter(meas.date >= "2016-08-24").\
        all()

    session.close()

    # Convert the list to Dictionary
    all_prcp = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a list of all Stations"""
    results = session.query(Station.station).\
        order_by(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return a list of all TOBs"""
    results = session.query(meas.date,  meas.tobs,meas.prcp).\
                filter(meas.date >= '2016-08-23').\
                filter(meas.station=='USC00519281').\
                order_by(meas.date).all()

    session.close()

    # Convert the list to Dictionary
    all_tobs = []
    for prcp, date,tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    session = Session(engine)

    """Return a list of min, avg and max tobs for a start date"""
    results = session.query(func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)).\
                filter(meas.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    session = Session(engine)

    """Return a list of min, avg and max tobs for start and end dates"""
    results = session.query(func.min(meas.tobs), func.avg(meas.tobs), func.max(meas.tobs)).\
                filter(meas.date >= start_date).\
                filter(meas.date <= end_date).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    
    return jsonify(start_end_tobs)
    
if __name__ == '__main__':
    app.run(debug=True)