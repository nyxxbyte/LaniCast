import os
import requests
from django.shortcuts import render

def weather_view(request):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = request.GET.get("city", "Puerto Princesa").strip()
    
    if not city:
        city = "Puerto Princesa"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    weather_data = {}

    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 404:
            weather_data = {"error": f"City '{city}' not found."}
        elif response.status_code == 401:
            weather_data = {"error": "Invalid API key or key is not active yet."}
        else:
            response.raise_for_status()
            data = response.json()
            weather_data = {
                "city": data.get("name"),
                "country": data.get("sys", {}).get("country"),
                "temp": round(data.get("main", {}).get("temp", 0)),
                "feels_like": round(data.get("main", {}).get("feels_like", 0)),
                "humidity": data.get("main", {}).get("humidity"),
                "wind_speed": round(data.get("wind", {}).get("speed", 0) * 3.6, 1),
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
            }
    except requests.exceptions.RequestException:
        weather_data = {"error": "Failed to connect to the weather service."}
    except (KeyError, IndexError):
        weather_data = {"error": "Received invalid data from the weather service."}

    return render(request, "weather.html", {"weather": weather_data, "city": city})