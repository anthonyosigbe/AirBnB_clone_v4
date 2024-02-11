#!/usr/bin/python3
"""
Flask application integrated with an AirBnB static HTML template.
"""
from flask import Flask, render_template, url_for
from models import storage
import uuid;

# Flask configuration setup.
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


# Start rendering Flask pages.
@app.teardown_appcontext
def teardown_db(exception):
    """
    Following each request, this method calls `.close()`
    (i.e., `.remove()`) on the current SQLAlchemy Session.
    """
    storage.close()


@app.route('/101-hbnb')
def hbnb_filters(the_id=None):
    """
    Manages requests to a custom template
    containing states, cities, and amenities.
    """
    state_objs = storage.all('State').values()
    states = dict([state.name, state] for state in state_objs)
    amens = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                 for user in storage.all('User').values())
    return render_template('101-hbnb.html',
                           cache_id=uuid.uuid4(),
                           states=state_objs,
                           amens=amens,
                           places=places,
                           users=users)

if __name__ == "__main__":
    """Primary Flask application."""
    app.run(host=host, port=port)
