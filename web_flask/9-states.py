#!/usr/bin/python3


import os
import sys  # Import the sys module

# Get the directory path of the current script
current_directory = os.path.dirname(os.path.realpath(__file__))

# Append the directory containing the 'models' module to the Python path
models_directory = os.path.join(current_directory, 'models')
sys.path.append(models_directory)

# Now you can continue with the rest of your script
# ...

"""Importing Flask to run the web app"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_storage(exception):
    """ Method to close the session """
    storage.close()


@app.route('/states', strict_slashes=False)
def state():
    """Displays an HTML page with states"""
    states = storage.all(State)
    return render_template('9-states.html', states=states, mode='all')


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """Displays an HTML page with cities of that state"""
    requested_state = None
    for state in storage.all(State).values():
        if state.id == id:
            requested_state = state
            break
    if requested_state:
        return render_template('9-states.html', states=requested_state, mode='id')
    else:
        return render_template('9-states.html', states=None, mode='none')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

