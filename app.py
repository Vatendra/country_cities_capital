from flask import Flask, render_template, request
from database import Database
app = Flask(__name__)
db = Database('data.json')


@app.route('/')
def home():  # put application's code here
    data = db.get_country_data()
    return render_template('index.html', data=data)


@app.route('/get_states', methods=['POST'])
def country():
    # retrieve data from POST
    country_id = request.form['country_id']
    # get state data
    data = db.get_state_data(country_id)
    return {'states': data}


@app.route('/get_cities', methods=['POST'])
def state():
    # retrieve data from POST
    state_id = request.form['state_id']
    # get city data
    data = db.get_city_data(state_id)
    return {'cities': data}


if __name__ == '__main__':
    app.run()
