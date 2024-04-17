# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil import parser, relativedelta
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

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

#1 Define a route for the homepage and list all available routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

#2 Convert the query results from my precipitation analysis (the last 12 months of data)
#to a dictionary using date as the key and prcp as the value. 

#Route to retrieve precipitation data for the last 12 months
@app.route("/api/v1.0/precipitation")  # Define a route for precipitation data
def get_precipitation():
    # Calculating start date 12 months before end date
    start_date = end_date - relativedelta.relativedelta(months=12)
    # Querying precipitation data for the last 12 months
    precipitations = session.query(Measurement.prcp, Measurement.date
                                  ).filter(Measurement.date >= start_date, 
                                           Measurement.date <= end_date).all()
    all_precipitations = [{"date": date, "precipitation": prcp} for prcp, date in precipitations]  
    
    return jsonify(all_precipitations)
    
#3 Return a JSON list of stations from the dataset.
# Define a route for station data first
@app.route("/api/v1.0/stations") 
def get_stations():
    results = session.query(Station.station).all()
    stations_list = list(np.ravel(results)) 
    return jsonify(stations_list)

#4 Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs") # Define a route for temperature observations
def waihee():
    start_date = end_date - relativedelta.relativedelta(months=12)  
    station_id = "USC00519281"  
    waihee_query = session.query(Measurement.tobs).filter(and_(Measurement.date >= start_date,
                                                               Measurement.date <= end_date))
    # Extract temperatures from the query results
    temperatures = [temp[0] for temp in waihee_query]
    
    # Return a JSON list of temperature observations for the previous year.                                                           Measurement.station == station_id)).all()
    return jsonify(temperatures)  

#5 Return a JSON list of the minimum temperature, 
# the average temperature, and the maximum temperature for a specified start-end range. 
@app.route("/api/v1.0/start_end/<start_date>/<end_date>")
def start_end_route(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d") 
    end_date = datetime.strptime(end_date, "%Y-%m-%d")  
    
    temp_stats = session.query(
        func.min(Measurement.tobs).label('min_temp'),
        func.max(Measurement.tobs).label('max_temp'),
        func.avg(Measurement.tobs).label('avg_temp')
    ).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    # Extract values from the query results
    min_temp, max_temp, avg_temp = temp_stats[0]

    # Create a dictionary to hold the temperature stats
    temp_data = {
        "TMIN": min_temp,
        "TAVG": avg_temp,
        "TMAX": max_temp
    }
    
    return jsonify(temp_data)

# Run the Flask app on port 5001
if __name__ == '__main__':
    app.run(debug=True, port=5001)

# Close out the session
session.close()