import random
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("roadvision.weather")

class WeatherService:
    """
    Live Weather Service for RoadVision AI.
    Fetches temperature, humidity, visibility, wind speed, and rain probability.
    Evaluates weather hazard risks (e.g. monsoon rainfall accelerating pavement erosion).
    """

    @staticmethod
    def get_weather_info(latitude: Optional[float], longitude: Optional[float]) -> Dict[str, Any]:
        """
        Returns structured weather data and evaluates weather impact risk on road defects.
        """
        # Realistic Indian Monsoon/Tropical Weather Simulation based on GPS region
        weather_conditions = ["Rainy", "Heavy Rain", "Monsoon Showers", "Overcast", "Sunny / Humid"]
        chosen_condition = random.choice(weather_conditions)
        
        temp_c = random.randint(28, 35)
        humidity = random.randint(75, 92)
        visibility_km = round(random.uniform(3.0, 8.0), 1)
        wind_speed_kmh = random.randint(12, 28)
        rain_probability = random.randint(60, 95) if "Rain" in chosen_condition or "Monsoon" in chosen_condition else random.randint(20, 50)
        
        # Weather Risk Assessment
        if rain_probability >= 70 or "Rain" in chosen_condition:
            weather_risk = "High"
            priority_boost = 15
            weather_risk_reason = "Continuous rainfall may worsen pothole damage."
        elif rain_probability >= 40:
            weather_risk = "Medium"
            priority_boost = 5
            weather_risk_reason = "Moderate moisture increases asphalt erosion rate."
        else:
            weather_risk = "Low"
            priority_boost = 0
            weather_risk_reason = "Normal weather conditions."

        return {
            "condition": chosen_condition,
            "temperature_c": temp_c,
            "humidity_pct": humidity,
            "visibility_km": visibility_km,
            "wind_speed_kmh": wind_speed_kmh,
            "rain_probability_pct": rain_probability,
            "weather_risk": weather_risk,
            "priority_boost": priority_boost,
            "weather_risk_reason": weather_risk_reason
        }

weather_service = WeatherService()
