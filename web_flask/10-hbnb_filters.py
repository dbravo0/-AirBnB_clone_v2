#!/usr/bin/python3
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(error):
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    states = storage.all(State).values()
    cities = storage.all(City).values()
    amenities = storage.all(Amenity).values()
    sort_states = sorted(list(states), key=lambda k: k.name)
    sort_cities = sorted(list(cities), key=lambda k: k.name)
    sort_amenities = sorted(list(amenities), key=lambda k: k.name)
    return render_template('10-hbnb_filters.html', states=sort_states,
                           cities=sort_cities, amenities=sort_amenities)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
