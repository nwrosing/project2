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

@app.route("/metadata/state/<state>")
def overdose_by_state(state):
    """Return the MetaData for a given sample."""
    sel = [
        overdose_metadata.State,
        overdose_metadata.Year,
        overdose_metadata.Prescription_Deaths,
        overdose_metadata.Population,
        overdose_metadata.Crude_Rate_Per_100000,
        overdose_metadata.StateAbbr,
        overdose_metadata.Prescribing_Rate_Per_100,
    ]

    results = db.session.query(*sel).all()

    # Create a Dictionary Entry for each Row of Metadata Information
    overdose_by_state = {}
    for result in results:
        overdose_by_state["State"] = result[0]
        overdose_by_state["Year"] = result[1]
        overdose_by_state["Prescription_Deaths"] = result[2]
        overdose_by_state["Population"] = result[3]
        overdose_by_state["Crude_Rate_Per_100000"] = result[4]
        overdose_by_state["StateAbbr"] = result[5]
        overdose_by_state["Prescribing_Rate_Per_100"] = result[6]

    print(overdose_by_state)
    return jsonify(overdose_by_state)


if __name__ == "__main__":
    app.run()
