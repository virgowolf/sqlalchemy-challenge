# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:/Resources///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

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

#Start at the homepage. List all the available routes.

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/measurement<br/>"
        f"/api/v1.0/station"
    )


#/api/v1.0/precipitation 
from dateutil import parser, relativedelta

# Parse the end date into a datetime object
end_date = parser.parse('2017-08-23')

# Calculate the start date by subtracting 12 months from the end date
start_date = end_date - relativedelta.relativedelta(months=12)

# Query using the calculated start and end dates
precipitations = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

# Create a list of tuples containing the precipitation and date data
precip_data = [(precipitation.prcp, precipitation.date) for precipitation in precipitations]

session.close()

#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
all_precipitations = []
for date in precipitation:
	precip_dictionary = {}
	precip_dictionary["date"] = date
	precip_dictionary["precipitation"] = pcrp
	all_precipitations.append(precip_dictionary)
	

#Return the JSON representation of your dictionary.
return jsonify(all_precipitations)

if __name__ == '__main__':
    app.run(debug=True)

