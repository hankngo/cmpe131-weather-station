from flask import Flask, request, jsonify, render_template, redirect, url_for
import datetime

app = Flask(__name__)

weather_data = []

@app.route('/')
def home():
    return render_template('index.html', weather_data=weather_data)

@app.route('/add', methods=['POST'])
def add_weather_data():
    temperature = request.form['temperature']
    humidity = request.form['humidity']
    data = {
        'date': datetime.datetime.now(),
        'temperature': temperature,
        'humidity': humidity
    }
    weather_data.append(data)
    return redirect(url_for('home'))  # Redirect to the home page to see the updated list

@app.route('/analysis')
def analysis():
    # Ensure there is weather data to analyze
    if not weather_data:
        return jsonify({"error": "No weather data available"}), 404
    # Calculate the average temperature
    total_temp = sum(float(data['temperature']) for data in weather_data)
    average_temp = total_temp / len(weather_data)
    # Return the analysis results as JSON
    return jsonify({"average_temperature": average_temp})

if __name__ == '__main__':
    app.run(debug=True)