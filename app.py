from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

# Simulated in-memory database
weather_data = []

@app.route('/')
def home():
    return render_template('index.html', weather_data=weather_data)

@app.route('/add', methods=['POST'])
def add_weather_data():
    data = {
        'date': datetime.datetime.now(),
        'temperature': request.json['temperature'],
        'humidity': request.json['humidity']
    }
    weather_data.append(data)
    return jsonify(data)

@app.route('/data')
def get_weather_data():
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)