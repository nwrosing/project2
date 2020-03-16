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
Samples_Metadata = Base.classes.sample_metadata

#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/metadata/state/<state>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.State,
        Samples_Metadata.Year,
        Samples_Metadata.Prescription_Deaths,
        Samples_Metadata.Population,
        Samples_Metadata.Crude_Rate_Per_100000,
        Samples_Metadata.StateAbbr,
        Samples_Metadata.Prescribing_Rate_Per_100,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a Dictionary Entry for each Row of Metadata Information
    sample_metadata = {}
    for result in results:
        sample_metadata["State"] = result[0]
        sample_metadata["Year"] = result[1]
        sample_metadata["Prescription_Deaths"] = result[2]
        sample_metadata["Population"] = result[3]
        sample_metadata["Crude_Rate_Per_100000"] = result[4]
        sample_metadata["StateAbbr"] = result[5]
        sample_metadata["Prescribing_Rate_Per_100"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)