from flask import Flask, render_template, request
import requests  # type: ignore
import joblib  # type: ignore
import numpy as np  # type: ignore

app = Flask(__name__, template_folder='my_templates')
model = joblib.load('temp_model.pkl')

API_KEY = "ebab3d399da1c49079f35277706aaf7a"
CITY = "Muranga"

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return {
        'max_temp': data["main"]["temp_max"],
        'humidity': data["main"]["humidity"],
        'rainfall': data.get('rain', {}).get('1h', 0)
    }

def generate_advice(temp, humidity, rainfall):
    advice = []
    if temp > 30:
        advice.append("High temperature, consider mulching (Joto kali, fikiria kutumia matandazo)")
    if humidity > 80:
        advice.append("High humidity, risk of fungal diseases (Unyevu mwingi, kuna hatari ya magonjwa ya kuvu).")
    if rainfall < 5:
        advice.append("Low rainfall, consider irrigation (Mvua ni kidogo, fikiria kumwagilia maji).")
    if rainfall > 20:
        advice.append("Heavy rain, risk of waterlogging (Mvua kubwa, kuna hatari ya mafuriko ya mashambani).")
    if 20 <= temp <= 30 and rainfall > 5:
        advice.append("Ideal conditions for planting, Soil moisture is sufficient (Hali nzuri kwa kupanda, unyevu wa udongo unatosha).")
    elif temp < 15:
        advice.append("Low temperatures, Delay planting as seed germination may be poor (Joto la chini, chelewesha kupanda kwani mbegu zinaweza zisichipue vizuri).")

    return advice

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city"]
        weather = get_weather_data(city)

        features = np.array([[weather['max_temp'], weather['humidity'], weather['rainfall']]])
        predicted_temp = model.predict(features)[0]
        predicted_temp = round(predicted_temp, 1)

        advice = generate_advice(predicted_temp, weather['humidity'], weather['rainfall'])

        return render_template("project_frontend.html",
                               weather=weather,
                               predicted_temp=predicted_temp,
                               advice=advice,
                               city=city)
    return render_template("project_frontend.html", weather=None)


# ❗ REMOVE debug & do not run using app.run() on Vercel
# Vercel will automatically detect `app` and serve it


