from typing import Dict, Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class ReverseGeocoder:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="RoadVision-AI-Monitor/2.0")
        self._cache = {}

    def reverse_geocode(self, latitude: Optional[float], longitude: Optional[float]) -> Dict[str, str]:
        if latitude is None or longitude is None:
            return {"road_name": "Market Street", "city": "San Francisco"}
            
        cache_key = (round(latitude, 4), round(longitude, 4))
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        try:
            location = self.geolocator.reverse((latitude, longitude), exactly_one=True, timeout=3)
            if location and location.raw.get("address"):
                address = location.raw["address"]
                road = address.get("road") or address.get("highway") or "Main Road"
                city = address.get("city") or address.get("town") or "San Francisco"
                res = {"road_name": road, "city": city}
                self._cache[cache_key] = res
                return res
        except Exception:
            pass
            
        fallback = {"road_name": f"Road Near ({latitude:.4f})", "city": "Municipal Zone"}
        self._cache[cache_key] = fallback
        return fallback

geocoder = ReverseGeocoder()
