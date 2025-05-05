import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
import os
import streamlit as st

def get_weather_forecast(city: str, days: int = 5) -> Optional[Dict]:
    """
    Get weather forecast for a city using OpenWeatherMap API.
    
    Args:
        city: City name
        days: Number of days to forecast (max 5)
        
    Returns:
        Dict: Weather forecast data or None if error
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            st.warning("OpenWeather API key not found. Weather information will not be available.")
            return None
            
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            forecast = []
            
            # Get daily forecasts
            for item in data["list"]:
                date = datetime.fromtimestamp(item["dt"])
                if len(forecast) < days:
                    forecast.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "temp": item["main"]["temp"],
                        "description": item["weather"][0]["description"],
                        "icon": item["weather"][0]["icon"]
                    })
            
            return {
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "forecast": forecast
            }
        else:
            st.warning(f"Weather data not available for {city}. Error: {response.status_code}")
    except Exception as e:
        st.warning(f"Error getting weather for {city}: {str(e)}")
    return None

def convert_currency(amount: float, from_currency: str, to_currency: str) -> Optional[float]:
    """
    Convert currency using Exchange Rates API.
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code
        to_currency: Target currency code
        
    Returns:
        float: Converted amount or None if error
    """
    try:
        api_key = os.getenv("EXCHANGERATES_API_KEY")
        if not api_key:
            st.warning("Exchange Rates API key not found. Currency conversion will not be available.")
            return None
            
        base_url = "https://api.exchangeratesapi.io/v1/latest"
        params = {
            "access_key": api_key,
            "base": from_currency,
            "symbols": to_currency
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "rates" in data and to_currency in data["rates"]:
                rate = data["rates"][to_currency]
                return amount * rate
            else:
                st.warning(f"Currency conversion not available for {from_currency} to {to_currency}")
        else:
            st.warning(f"Currency conversion failed. Error: {response.status_code}")
    except Exception as e:
        st.warning(f"Error converting currency: {str(e)}")
    return None

def get_currency_symbol(currency_code: str) -> str:
    """
    Get currency symbol for a currency code.
    
    Args:
        currency_code: Currency code (e.g., USD, EUR)
        
    Returns:
        str: Currency symbol
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "INR": "₹",
        "CNY": "¥",
        "AUD": "A$",
        "CAD": "C$"
    }
    return symbols.get(currency_code.upper(), currency_code) 