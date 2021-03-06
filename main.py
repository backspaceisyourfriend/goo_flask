import os
from datetime import datetime
import requests
from flask import Flask, render_template

app = Flask(__name__)

WEATHER_KEY = ""

def degrees_to_compass_direction(deg):
    val = int((deg / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)


@app.route('/weather')
def get_weather():

    zip_code = 59718
    country_code = "US"
    my_url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&units=imperial&appid={WEATHER_KEY}"

    resp = requests.get(my_url, params={})

    weather_data = resp.json()

    high_temp = round(weather_data['main']['temp_max'])
    low_temp = round(weather_data['main']['temp_min'])

    # using the APIs JSON data, return that to browser
    return render_template('index.html', title='Welcome', hi=high_temp, low=low_temp, wd=weather_data)


@app.route('/5day')
def get_5day():

    lat = "45.676998"
    lon = "-111.042931"
    my_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&units=imperial&appid={WEATHER_KEY}"
    resp = requests.get(my_url, params={})

    weather_data = resp.json()

    daily_data = weather_data['daily']

    for day in daily_data:
        day['sunrise'] = datetime.fromtimestamp(day['sunrise']).strftime("%H:%M:%S%p")
        day['sunset'] = datetime.fromtimestamp(day['sunset']).strftime("%H:%M:%S%p")
        day['dt'] = datetime.fromtimestamp(day['dt']).strftime("%m/%d/%Y")
        day['temp']['max'] = round(day['temp']['max'])
        day['temp']['min'] = round(day['temp']['min'])
        day['wind_gust'] = f"{round(day['wind_gust'])} mph"
        day['wind_dir'] = degrees_to_compass_direction(day['wind_deg'])
        day['extra'] = "extra stuff"

    # using the APIs JSON data, return that to browser
    return render_template('index.html', title='Welcome', wd=daily_data)


if __name__ == "__main__":
    WEATHER_KEY = os.getenv("WEATHER_KEY")
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
