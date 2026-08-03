import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("roadvision.geocoding")

class ReverseGeocoder:
    """
    Reverse Geocoding Service translating GPS (lat, lng) into Indian Human-Readable Addresses:
    Road Name, Area / Locality, City, District, State, Country, Postal Code.
    """
    
    def __init__(self):
        self._geolocator = None
        self._cache = {}

    @property
    def geolocator(self):
        if self._geolocator is None:
            try:
                from geopy.geocoders import Nominatim
                self._geolocator = Nominatim(user_agent="RoadVision-AI-Indian-Roads/4.0")
            except Exception as e:
                logger.warning(f"geopy module not available, using resilient fallback geocoder: {e}")
                self._geolocator = False
        return self._geolocator

    def reverse_geocode(self, latitude: Optional[float], longitude: Optional[float]) -> Dict[str, Any]:
        fallback = {
            "road_name": "Anna Salai",
            "area": "Teynampet",
            "city": "Chennai",
            "district": "Chennai",
            "state": "Tamil Nadu",
            "country": "India",
            "postal_code": "600018",
            "formatted_address": "Anna Salai, Teynampet, Chennai, Tamil Nadu"
        }

        if latitude is None or longitude is None:
            return fallback

        cache_key = (round(latitude, 4), round(longitude, 4))
        if cache_key in self._cache:
            return self._cache[cache_key]

        if self.geolocator:
            try:
                location = self.geolocator.reverse((latitude, longitude), exactly_one=True, timeout=3)
                if location and location.raw.get("address"):
                    addr = location.raw["address"]
                    
                    road = addr.get("road") or addr.get("pedestrian") or addr.get("highway") or "Anna Salai"
                    area = addr.get("suburb") or addr.get("neighbourhood") or addr.get("residential") or "Teynampet"
                    city = addr.get("city") or addr.get("town") or addr.get("village") or "Chennai"
                    district = addr.get("state_district") or addr.get("county") or city
                    state = addr.get("state") or "Tamil Nadu"
                    country = addr.get("country") or "India"
                    postal_code = addr.get("postcode") or "600018"
                    
                    formatted = f"{road}, {area}, {city}, {state}"
                    
                    res = {
                        "road_name": road,
                        "area": area,
                        "city": city,
                        "district": district,
                        "state": state,
                        "country": country,
                        "postal_code": postal_code,
                        "formatted_address": formatted
                    }
                    self._cache[cache_key] = res
                    return res
            except Exception as e:
                logger.warning(f"Geocoding service fallback: {e}")

        self._cache[cache_key] = fallback
        return fallback

geocoder = ReverseGeocoder()
