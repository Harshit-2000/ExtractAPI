from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
from werkzeug.wrappers.response import Response
from extract import Extract
from flask_cors import CORS

import os
import json


UPLOAD_FOLDER = os.path.dirname(
    os.path.abspath(__file__)) + '/uploads/'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/api/extract", methods=["POST"])
def upload():
    data = []
    if request.method == "POST":
        files = request.files.getlist("files[]")
        for file in files:
            if file.filename == '':
                continue
            tempdata = {}
            filename = secure_filename(file.filename)
            tempdata["filename"] = filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            Extract(filepath, tempdata)
            os.unlink('uploads/' + filename)
            data.append(tempdata)

        response = jsonify(data)
        return response


@app.route('/api/addname', methods=["POST"])
def addName():
    data = request.get_json()
    try:
        name = data['name']
        with open('data/names/newNames.txt', mode='a') as file:
            file.write(name + ' ')
        response = Response(json.dumps(
            {'message': 'success'}), status=201, mimetype='application/json')
        return response

    except Exception as e:
        print(e)
        response = Response(json.dumps(
            {'message': 'error'}), status=500, mimetype='application/json')
        return response
