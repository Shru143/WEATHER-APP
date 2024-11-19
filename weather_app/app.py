from flask import Flask, render_template, request
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.getenv('42cb6d4aa2bb90817c110c14ae2dc634')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        
        # Print for debugging
        print(f"Fetching weather data for city: {city}")
        
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        try:
            # Print API request URL for debugging
            print(f"Making request to: {BASE_URL}")
            
            response = requests.get(BASE_URL, params=params)
            
            # Print response status code for debugging
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 401:
                error = "Invalid API key. Please check your OpenWeatherMap API key."
                return render_template('index.html', error=error)
                
            if response.status_code == 404:
                error = f"City '{city}' not found. Please check the city name."
                return render_template('index.html', error=error)
                
            response.raise_for_status()
            
            weather_data = response.json()
            print(f"Weather data received: {weather_data}")  # Debug print
            
            weather_data['main']['temp'] = round(weather_data['main']['temp'])
            weather_data['sys']['sunrise'] = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
            weather_data['sys']['sunset'] = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')
            
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {str(e)}")  # Debug print
            error = "Error fetching weather data. Please check your internet connection and try again."
            
    return render_template('index.html', weather_data=weather_data, error=error)

if __name__ == '__main__':
    app.debug = True
    app.run()