import requests
import re
from datetime import datetime, timedelta, timezone
from pprint import pprint

class WeatherServiceSL:
    """Summarize data from OpenWeatherMap API for Sri Lanka

    This module retrieves weather information using OpenWeatherMap's API
    and returns a dictionary containing summarized weather data for the
    specified number of hours.

    Required:
        latitude - Degrees of latitude as a float (e.g., 6.9271 for Colombo)
        longitude - Degrees of longitude as a float (e.g., 79.8612 for Colombo)
        api_key - Your OpenWeatherMap API key.

    Optional:
        forecast_hours - Period of future time over which to summarize conditions.
        api_server - Defaults to OpenWeatherMap API endpoint.
    """

    def __init__(self, latitude=6.9271,
                       longitude=79.8612,
                       api_key="6b0acad8dab17f558fd453ddd23b2c06",
                       forecast_hours=12,
                       api_server="https://api.openweathermap.org/data/2.5/forecast",
                       debug=False):

        self.latitude = latitude
        self.longitude = longitude
        self.forecast_hours = forecast_hours
        self.api_key = api_key
        self.api_server = api_server
        self.debug = debug

    def fetch(self):
        # Fetch weather forecast data
        params = {
            'lat': self.latitude,
            'lon': self.longitude,
            'appid': self.api_key,
            'units': 'metric'  # Use metric units (Celsius for temperature)
        }
        response = requests.get(self.api_server, params=params)

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

        data = response.json()

        # Properties to summarize
        properties = ["pop", "main.temp", "main.humidity", "clouds.all", "wind.speed", "wind.gust"]

        # Summarize data over the forecast period
        summary = {
            'ave_probability_of_precipitation': 0,
            'total_precipitation': 0,
            'ave_relative_humidity': 0,
            'ave_sky_cover': 0,
            'ave_temperature': 0,
            'ave_wind_speed': 0,
            'ave_wind_gust': 0
        }

        end_time = datetime.now(timezone.utc) + timedelta(hours=self.forecast_hours)
        
        # Accumulate values
        count = 0
        for forecast in data['list']:
            forecast_time = datetime.fromtimestamp(forecast['dt'], tz=timezone.utc)
            if forecast_time > end_time:
                break

            count += 1
            summary['ave_probability_of_precipitation'] += forecast.get('pop', 0) * 100
            summary['ave_relative_humidity'] += forecast['main']['humidity']
            summary['ave_sky_cover'] += forecast['clouds']['all']
            summary['ave_temperature'] += forecast['main']['temp']
            summary['ave_wind_speed'] += forecast['wind'].get('speed', 0)
            summary['ave_wind_gust'] += forecast['wind'].get('gust', 0)

        if count > 0:
            summary['ave_probability_of_precipitation'] /= count
            summary['ave_relative_humidity'] /= count
            summary['ave_sky_cover'] /= count
            summary['ave_temperature'] /= count
            summary['ave_wind_speed'] /= count
            summary['ave_wind_gust'] /= count

        # Debug output
        if self.debug:
            pprint(summary)

        return summary


if __name__ == "__main__":
    # Replace "your_api_key_here" with your OpenWeatherMap API key
    weather = WeatherServiceSL(api_key="6b0acad8dab17f558fd453ddd23b2c06", debug=True)
    pprint(weather.fetch())
