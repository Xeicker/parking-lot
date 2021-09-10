import os
from flask import Flask, g
from flask_restful import Api
from Resources import CarList, CarResource
import logging

app = Flask(__name__)
api = Api(app)

# Define Resourses used by application
api.add_resource(CarList, "/cars")
api.add_resource(CarResource, "/cars/<string:identifier>")


# Close db when finishing request
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello():
    """Show Readme file on root URL"""

    with open("README.md", "r") as f:
        # Replace string new lines to html new lines
        text = f.read().replace("\n", "<br>")
    return text


def configure_logging():
    """Define logging characteristics"""

    del app.logger.handlers[:]

    # Define log formats
    formatter = logging.Formatter(
        "<------Event------>\
        \nTime: %(asctime)s\
        \nName: %(name)s\
        \nLevel: %(levelname)s\
        \nMessage: %(message)s\
        \n<---------------->")

    # Set logging file through a log handler
    info_handler = logging.FileHandler("info.log")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    # Set handlers to all loggers
    app.logger.addHandler(info_handler)
    app.logger.setLevel(logging.INFO)
    CarList.logger.addHandler(info_handler)
    CarList.logger.setLevel(logging.INFO)
    pass


# Run application on localhost:8080/
if __name__ == '__main__':
    configure_logging()
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
