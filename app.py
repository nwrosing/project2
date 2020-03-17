#################################################
# Flask Application
#################################################

# Dependencies and Setup
import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Connection Setup
#################################################
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/opioid_death_prescription2.sqlite"
db = SQLAlchemy(app)

# Reflect Existing Database Into a New Model
Base = automap_base()
# Reflect the Tables
Base.prepare(db.engine, reflect=True)

# Save References to Each Table
overdose_metadata = Base.classes.opioid_death_prescription2

#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/metadata/year/<year>")
def overdose_by_year(year):
    sel = [
        overdose_metadata.State,
        getattr(overdose_metadata, 'Y_'+year),
    ]

    results = db.session.query(*sel).all()

    # Format the data to send as json
    data = {
        "states": [result[0] for result in results],
        "year": [result[1] for result in results],
        "Prescription_Deaths": [result[2] for result in results],
        "Population": [result[3] for result in results],
        "Crude_Rate_Per_100000": [result[4] for result in results],
        "StateAbbr": [result[5] for result in results],
        "Prescribing_Rate_Per_100": [result[6] for result in results]
    }

    return jsonify(data)

@app.route("/metadata/state/<state>")
def overdose_by_state(state):

    stmt = db.session.query(overdose_metadata).statement

    df = pd.read_sql_query(stmt, db.session.bind)

    sample_data = df.loc[df['State'] == state, :]

    return jsonify(list(df.columns)[1:])

    data = {
        "states": [result[0] for result in results],
        "year": [result[1] for result in results],
        "Prescription_Deaths": [result[2] for result in results],
        "Population": [result[3] for result in results],
        "Crude_Rate_Per_100000": [result[4] for result in results],
        "StateAbbr": [result[5] for result in results],
        "Prescribing_Rate_Per_100": [result[6] for result in results]
    }

    return jsonify(data)

@app.route("/states")
def states():
    sel = [overdose_metadata.State]

    states = [state[0] for state in db.session.query(*sel).all()]

    return jsonify(states)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
