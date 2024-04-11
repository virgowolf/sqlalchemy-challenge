from flask import Flask, jsonify
from dateutil import parser, relativedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/measurement<br/>"
        f"/api/v1.0/station"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    end_date = parser.parse('2017-08-23')
    start_date = end_date - relativedelta.relativedelta(months=12)
    precipitations = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    all_precipitations = []
    for prcp, date in precipitations:
        precip_dictionary = {}
        precip_dictionary["date"] = date
        precip_dictionary["precipitation"] = prcp
        all_precipitations.append(precip_dictionary)
    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations_list = list(np.ravel(results))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def waihee():
    end_date = parser.parse('2017-08-23')
    start_date = end_date - relativedelta.relativedelta(months=12)
    station_id="USC00519281"
    waihee_query = session.query(Measurement.tobs).filter(and_(Measurement.date >= start_date, Measurement.date <= end_date, Measurement.station == station_id)).all()
    return jsonify(waihee_query)

@app.route("/api/v1.0/<start>")
def start(start):
    sel = [
        Measurement.station,
        func.min(Measurement.tobs).label('min_temp'),
        func.max(Measurement.tobs).label('max_temp'),
        func.avg(Measurement.tobs).label('avg_temp')
    ]
    start_date = start
    end_date = '2015-11-01'  
    temp_query = session.query(*sel).filter_by(station="USC00519281").filter(and_(Measurement.date >= start_date, Measurement.date <= end_date)).all()
    temp_data = []
    for result in temp_query:
        station, min_temp, max_temp, avg_temp = result
        temp_data.append({
            "station": station,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": avg_temp
        })
    return jsonify(temp_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    sel = [
        Measurement.station,
        func.min(Measurement.tobs).label('min_temp'),
        func.max(Measurement.tobs).label('max_temp'),
        func.avg(Measurement.tobs).label('avg_temp')
    ]
    start_date = start
    end_date = end
    temp_query = session.query(*sel).filter_by(station="USC00519281").filter(and_(Measurement.date >= start_date, Measurement.date <= end_date)).all()
    temp_data = []
    for result in temp_query:
        station, min_temp, max_temp, avg_temp = result
        temp_data.append({
            "station": station,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": avg_temp
        })
    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


