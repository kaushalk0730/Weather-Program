#!/usr/bin/env python3
"""
Weather Forecast Program
A simple terminal-based program that fetches 7-day weather forecasts using Open-Meteo API.
"""

import requests
import json
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

def get_coordinates(city, state):
    """
    Get latitude and longitude coordinates for a city and state using Nominatim geocoding.
    
    Args:
        city (str): City name
        state (str): State abbreviation (e.g., 'TX')
    
    Returns:
        tuple: (latitude, longitude) or (None, None) if not found
    """
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(f"{city}, {state}, USA")
        
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
            
    except Exception as e:
        print(f"Error getting coordinates: {e}")
        return None, None

def get_weather_forecast(latitude, longitude):
    """
    Get 7-day weather forecast for given coordinates using Open-Meteo API.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    
    Returns:
        dict: Weather forecast data or None if error
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "timezone": "auto",
            "forecast_days": 7,
            "temperature_unit": "fahrenheit"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None
    except Exception as e:
        print(f"Error processing weather data: {e}")
        return None

def get_weather_condition(weather_code):
    """
    Convert weather code to human-readable condition.
    
    Args:
        weather_code (int): Weather code from Open-Meteo
    
    Returns:
        str: Weather condition description
    """
    weather_conditions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    
    return weather_conditions.get(weather_code, "Unknown")

def format_date(date_string):
    """
    Format date string to a more readable format.
    
    Args:
        date_string (str): Date in YYYY-MM-DD format
    
    Returns:
        str: Formatted date string
    """
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        return date_obj.strftime("%A, %B %d")
    except ValueError:
        return date_string

def display_forecast(weather_data, city, state):
    """
    Display the 7-day weather forecast in a formatted way.
    
    Args:
        weather_data (dict): Weather forecast data from API
        city (str): City name
        state (str): State abbreviation
    """
    if not weather_data or "daily" not in weather_data:
        print("Error: Could not retrieve weather data.")
        return
    
    daily = weather_data["daily"]
    dates = daily["time"]
    max_temps = daily["temperature_2m_max"]
    min_temps = daily["temperature_2m_min"]
    weather_codes = daily["weather_code"]
    
    print(f"\n🌤️  7-Day Weather Forecast for {city}, {state}")
    print("=" * 50)
    
    for i in range(len(dates)):
        date = format_date(dates[i])
        max_temp = round(max_temps[i])
        min_temp = round(min_temps[i])
        condition = get_weather_condition(weather_codes[i])
        
        print(f"{date}")
        print(f"  High: {max_temp}°F  Low: {min_temp}°F")
        print(f"  Condition: {condition}")
        print()

def main():
    """
    Main function to run the weather forecast program.
    """
    print("🌤️  Weather Forecast Program")
    print("=" * 30)
    
    while True:
        try:
            # Get user input
            location_input = input("\nEnter city and state (e.g., 'Austin, TX'): ").strip()
            
            if not location_input:
                print("Please enter a valid city and state.")
                continue
            
            # Parse input
            if "," not in location_input:
                print("Please use the format 'City, State' (e.g., 'Austin, TX')")
                continue
            
            city, state = location_input.split(",", 1)
            city = city.strip()
            state = state.strip().upper()
            
            print(f"\nLooking up coordinates for {city}, {state}...")
            
            # Get coordinates
            lat, lon = get_coordinates(city, state)
            
            if lat is None or lon is None:
                print(f"Could not find coordinates for {city}, {state}.")
                print("Please check the spelling and try again.")
                continue
            
            print(f"Found coordinates: {lat:.4f}, {lon:.4f}")
            print("Fetching weather data...")
            
            # Get weather forecast
            weather_data = get_weather_forecast(lat, lon)
            
            if weather_data:
                display_forecast(weather_data, city, state)
            else:
                print("Failed to retrieve weather data. Please try again.")
            
            # Ask if user wants to check another location
            while True:
                another = input("\nCheck another location? (y/n): ").strip().lower()
                if another in ['y', 'yes']:
                    break
                elif another in ['n', 'no']:
                    print("Thanks for using the Weather Forecast Program! 🌤️")
                    return
                else:
                    print("Please enter 'y' or 'n'.")
        
        except KeyboardInterrupt:
            print("\n\nThanks for using the Weather Forecast Program! 🌤️")
            return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
