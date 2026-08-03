import logging
from typing import Dict, Any, Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

logger = logging.getLogger("roadvision.geocoding")

class ReverseGeocoder:
    """
    Reverse Geocoding utility integrating OpenStreetMap Nominatim with local memory caching.
    Translates raw GPS (lat, lng) into administrative locations (Road Name, City, District, State).
    """
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="RoadVision-AI-SmartCity-Monitor/1.0")
        self._cache = {}

    def reverse_geocode(self, latitude: Optional[float], longitude: Optional[float]) -> Dict[str, Optional[str]]:
        """
        Performs reverse geocoding with caching and fallback handling.
        """
        if latitude is None or longitude is None:
            return {
                "road_name": "Unknown Road",
                "city": "Unknown City",
                "district": "Unknown District",
                "state": "Unknown State",
                "country": "Unknown Country",
                "formatted_address": "GPS Location Unavailable"
            }
            
        cache_key = (round(latitude, 4), round(longitude, 4))
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        try:
            location = self.geolocator.reverse((latitude, longitude), exactly_one=True, timeout=3)
            if location and location.raw.get("address"):
                address = location.raw["address"]
                road = address.get("road") or address.get("pedestrian") or address.get("highway") or "Main Road"
                city = address.get("city") or address.get("town") or address.get("village") or "Metropolis"
                district = address.get("state_district") or address.get("county") or "Central District"
                state = address.get("state") or "State Province"
                country = address.get("country") or "Country"
                
                res = {
                    "road_name": road,
                    "city": city,
                    "district": district,
                    "state": state,
                    "country": country,
                    "formatted_address": location.address
                }
                self._cache[cache_key] = res
                return res
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.warning(f"Geocoding service timeout/error: {e}")
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            
        # Fallback response
        fallback = {
            "road_name": f"Road Near ({latitude:.4f}, {longitude:.4f})",
            "city": "Municipal City",
            "district": "District Zone",
            "state": "State Region",
            "country": "Country",
            "formatted_address": f"Lat: {latitude:.4f}, Lng: {longitude:.4f}"
        }
        self._cache[cache_key] = fallback
        return fallback

geocoder = ReverseGeocoder()
