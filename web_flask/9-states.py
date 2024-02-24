#!/usr/bin/python3

from flask import Flask, render_template, abort
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def close_storage(exception):
    storage.close()

@app.route('/states', strict_slashes=False)
def get_states():
    try:
        states = storage.all(State)
        return render_template('9-states.html', states=states, mode='all')
    except Exception as e:
        app.logger.error('An error occurred: {}'.format(str(e)))
        abort(500)

@app.route('/states/<id>', strict_slashes=False)
def get_state_by_id(id):
    try:
        state = storage.get(State, id)
        if state:
            return render_template('9-states.html', states=state, mode='id')
        else:
            abort(404)
    except Exception as e:
        app.logger.error('An error occurred: {}'.format(str(e)))
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

