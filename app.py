"""
A sample Hello World server.
"""
import os

from flask import Flask, render_template,g
from flask_restful import Resource, Api, reqparse
import Resources

# pylint: disable=C0103
app = Flask(__name__)

api = Api(app)
#Define Resourses used by application
api.add_resource(Resources.CarList,"/cars")
api.add_resource(Resources.Car,"/cars/<string:identifier>")

#Close db when finishing request
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#Show Readme file on root URL
@app.route('/')
def hello():
    with open("README.md","r") as f:
        #Replace string new lines to html new lines
        text = f.read().replace("\n","<br>")
    return text

#Run application on localhost:8080/
if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
