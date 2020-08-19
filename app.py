# Imports
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################
#DATABASE SETUP#
################

# Create Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

#save references for each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################
#FLASK SETUP#
################

app = Flask(__name__)

#################
#FLASK ROUTES#
################


#first route
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'start-date'<br/>"
        f"/api/v1.0/'start-date'/'end-date'<br/>"
    )


#2nd Route
@app.route("/api/v1.0/precipitation")
def prec():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    
    key_value = {} 
    list_key = [result[0] for result in results]
    list_value = [result[1] for result in results]  
    lenList = len(list_key) 
    for elements in range(0,lenList): 
	    key = list_key[elements] 
	    value = list_value[elements] 
	    key_value[key] = value 

    return jsonify(key_value)


#3rd Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    return jsonify(results)

#4th Route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    import datetime as dt
    date = dt.datetime(2016, 8, 23)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > date).\
        filter(Measurement.station == 'USC00519281').all()
    session.close()
    
    return jsonify(results)

#5th Route
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    from datetime import datetime, timedelta
    startdate = datetime.strptime(start, "%Y-%m-%d")
    enddate = datetime.strptime("2017-08-23", "%Y-%m-%d")

    delta = enddate - startdate
    date_range = []
    for i in range(delta.days + 1):
        date_range.append(startdate + timedelta(days=i))
    
    str_date_range = []
    for date in date_range:
        new_date = date.strftime("%Y-%m-%d")
        str_date_range.append(new_date)

    tavg = session.query(func.avg(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]
    tmin = session.query(func.min(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]
    tmax = session.query(func.max(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]

    temp_dict = {}
    temp_dict["Average Temperature"] = tavg
    temp_dict["Minimum Temperature"] = tmin
    temp_dict["Maximum Temperature"] = tmax

    session.close()

    return jsonify(temp_dict)

#6th Route
@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    session = Session(engine)
    from datetime import datetime, timedelta
    startdate = datetime.strptime(start, "%Y-%m-%d")
    enddate = datetime.strptime(end, "%Y-%m-%d")


    delta = enddate - startdate
    date_range = []
    for i in range(delta.days + 1):
        date_range.append(startdate + timedelta(days=i))
    
    str_date_range = []
    for date in date_range:
        new_date = date.strftime("%Y-%m-%d")
        str_date_range.append(new_date)

    tavg = session.query(func.avg(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]
    tmin = session.query(func.min(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]
    tmax = session.query(func.max(Measurement.tobs))\
                .filter(Measurement.date.in_(str_date_range))[0][0]

    temp_dict = {}
    temp_dict["Average Temperature"] = tavg
    temp_dict["Minimum Temperature"] = tmin
    temp_dict["Maximum Temperature"] = tmax

    session.close()

    return jsonify(temp_dict)


if __name__ == '__main__':
    app.run(debug=True)