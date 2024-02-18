#!/usr/bin/python3
""" Write a script that starts a Flask web application,
Web application is listening on 0.0.0.0, port 5000 """

from models import storage
from models.state import State
from flask import Flask, render_template
from flask import abort

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def state_list():
    """state_list"""
    states = storage.all(State).values()
    return render_template(
        "9-states.html",
        states=states,
        condition="states_list")


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """states_by_id"""
    all_states = storage.all(State)
    state = all_states.get(id)
    if state is None:
        abort(404)
    return render_template(
        '9-states.html',
        state=state,
        condition="state_id")


@app.teardown_appcontext
def teardown(exception):
    """Removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

