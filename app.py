from flask import Flask, render_template, request
from database import Database
app = Flask(__name__)
db = Database('data.json')


@app.route('/')
def home():  # put application's code here
    data = db.get_country_data()
    return render_template('index.html', data=data)


@app.route('/get_states')
def country(country_id):
    # retrieve data from POST
    country_id = request.form['country_id']
    # get state data
    data = db.get_state_data(country_id)
    print('data:', data)
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()
