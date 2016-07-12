from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps


app = Flask(__name__)

# MONGODB_HOST, MONGODB_PORT, DBS_NAME, COLLECTION_NAME are the constants.
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'donorsUSA'
COLLECTION_NAME = 'projects'
FIELDS = {'funding_status': True, 'school_state': True, 'primary_focus_area': True, 'resource_type': True, 'poverty_level': True,
          'date_posted': True, 'total_donations': True, '_id': False}

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/donorsUS/projects")
def donor_projects():
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS, limit=5000)
    json_projects = []
    # json_projects is an array of key/value pair objects.
    for project in projects:
        json_projects.append(project)
    # Use with json.dumps to allow Python sets to be encoded to JSON
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects


if __name__ == '__main__':
    app.run(debug=True)
