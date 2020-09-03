#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models import State

app = Flask(__name__)


@app.teardown_appcontext
def closedb(foo):
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    state = states = None
    if not id:
        states = list(storage.all(State).values())
    else:
        states = storage.all(State)
        key = "State." + id
        if key in states:
            state = states[key]
        else:
            state = None
        states = []
    return render_template('9-states.html', states=states, state=state, id=id)


if __name__ == '__main__':
    storage.reload()
    app.run("0.0.0.0", 5000)
