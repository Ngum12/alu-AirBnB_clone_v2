#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the session"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """ display a HTML page: (inside the tag BODY) """
    states = sorted(list(storage.all(State).values()),
                    key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """ display a HTML page: (inside the tag BODY) """
    states = storage.all(State, id)
    if states:
        cities = sorted(states.cities, key=lambda city: city.name)
        return render_template('9-states.html', state=states, cities=cities)
    else:
        return render_template('9-states.html', state=None, cities=None)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
