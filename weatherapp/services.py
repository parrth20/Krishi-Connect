import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def describe_weather(code):
    return WEATHER_CODES.get(code, "Changing weather")


def geocode_city(city):
    city = (city or "").strip()
    if not city:
        return None

    response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=8,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results") or []
    if not results:
        return None

    result = results[0]
    return {
        "name": result.get("name"),
        "state": result.get("admin1"),
        "country": result.get("country"),
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "timezone": result.get("timezone") or "auto",
    }


def _safe_list_value(values, index=0):
    if isinstance(values, list) and len(values) > index:
        return values[index]
    return None


def get_weather_summary(city, forecast_days=5):
    try:
        location = geocode_city(city)
        if not location:
            return {"error": f"Could not find weather location for '{city}'."}

        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                ]
            ),
            "hourly": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation_probability",
                    "precipitation",
                    "weather_code",
                ]
            ),
            "daily": ",".join(
                [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_sum",
                    "precipitation_probability_max",
                ]
            ),
            "timezone": "auto",
            "forecast_days": forecast_days,
        }
        response = requests.get(FORECAST_URL, params=params, timeout=8)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        return {"error": f"Weather API request failed: {exc}"}

    current = data.get("current") or {}
    hourly = data.get("hourly") or {}
    daily = data.get("daily") or {}
    current_code = current.get("weather_code")

    current_summary = {
        "time": current.get("time"),
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "precipitation": current.get("precipitation"),
        "precipitation_probability": _safe_list_value(hourly.get("precipitation_probability")),
        "wind_speed": current.get("wind_speed_10m"),
        "weather_code": current_code,
        "condition": describe_weather(current_code),
    }

    days = []
    for index, date_value in enumerate(daily.get("time") or []):
        code = _safe_list_value(daily.get("weather_code"), index)
        days.append(
            {
                "date": date_value,
                "condition": describe_weather(code),
                "temperature_max": _safe_list_value(daily.get("temperature_2m_max"), index),
                "temperature_min": _safe_list_value(daily.get("temperature_2m_min"), index),
                "rain_mm": _safe_list_value(daily.get("precipitation_sum"), index),
                "rain_probability": _safe_list_value(daily.get("precipitation_probability_max"), index),
            }
        )

    return {
        "location": location,
        "current": current_summary,
        "daily": days,
        "source": "Open-Meteo",
    }


def build_farm_weather_advice(summary):
    if not summary or summary.get("error"):
        return ["Weather advice is unavailable right now. Try again after checking the city name."]

    current = summary.get("current", {})
    humidity = current.get("humidity")
    rain_probability = current.get("precipitation_probability")
    wind_speed = current.get("wind_speed")
    temperature = current.get("temperature")

    advice = []
    if rain_probability is not None and rain_probability >= 60:
        advice.append("Do not spray today unless the forecast gives a long dry window; rain can wash chemicals away.")
    elif rain_probability is not None and rain_probability >= 35:
        advice.append("Keep spraying only for a dry 6-8 hour window and check the sky before mixing chemicals.")
    else:
        advice.append("Rain risk looks manageable; field inspection and routine work are possible.")

    if humidity is not None and humidity >= 85:
        advice.append("High humidity can increase fungal disease risk; inspect lower leaves closely.")

    if wind_speed is not None and wind_speed >= 20:
        advice.append("Wind is high for spraying; drift can waste chemical and damage nearby crops.")

    if temperature is not None and temperature >= 35:
        advice.append("Heat stress risk is high; irrigate early morning or evening and avoid midday spraying.")

    return advice
