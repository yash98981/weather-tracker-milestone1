```python

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class WeatherAPIError(Exception):
    """Custom exception for weather API related errors"""
    def __init__(self, message: str, status_code: Optional[int] = None, url: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.url = url
        super().__init__(self.message)
    
    def __str__(self):
        if self.status_code:
            return f"{self.message} (Status: {self.status_code}, URL: {self.url})"
        return self.message

class LocationNotFoundError(WeatherAPIError):
    """Raised when weather location is not found"""
    def __init__(self, location: str, **kwargs):
        message = f"Weather location not found: {location}"
        super().__init__(message, **kwargs)

class WeatherClient:
  
    
    def __init__(self):
        """Initialize the weather client with API endpoints"""
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create HTTP session with retry logic and timeout"""
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        session = requests.Session()
        
        # Set up retry strategy for resilient API calls
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        return session
    
    def get_coordinates(self, city: str, country: str = "") -> Dict:
        """
        Get latitude and longitude coordinates for a city.
        
        Args:
            city: Name of the city
            country: Country code (optional)
        
        Returns:
            Dictionary with latitude, longitude, and location info
            
        Raises:
            LocationNotFoundError: If the location is not found
            WeatherAPIError: For other API errors
        """
        # Prepare query parameters
        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        if country:
            params["country"] = country
        
        try:
            print(f" Making geocoding request for: {city}, {country}")
            print(f" Request URL: {self.geocoding_url}")
            print(f" Parameters: {params}")
            
            # Make the HTTP request
            response = self.session.get(
                self.geocoding_url,
                params=params,
                timeout=10
            )
            
            print(f" Response Status Code: {response.status_code}")
            print(f" Final URL: {response.url}")
            
            # Handle HTTP errors
            if not response.ok:
                raise WeatherAPIError(
                    f"Geocoding API request failed: {response.reason}",
                    status_code=response.status_code,
                    url=str(response.url)
                )
            
            
            data = response.json()
            print(f" Raw Response: {json.dumps(data, indent=2)}")
            
            # Check if any results were found
            if not data.get("results"):
                raise LocationNotFoundError(f"{city}, {country}")
            
            # Extract first result
            location = data["results"][0]
            result = {
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "name": location["name"],
                "country": location.get("country", ""),
                "timezone": location.get("timezone", ""),
                "elevation": location.get("elevation", 0)
            }
            
            print(f" Successfully found coordinates: {result}")
            return result
            
        except requests.exceptions.Timeout:
            raise WeatherAPIError("Request timed out", url=self.geocoding_url)
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Connection failed", url=self.geocoding_url)
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Request failed: {e}", url=self.geocoding_url)
        except json.JSONDecodeError:
            raise WeatherAPIError("Invalid JSON response", url=str(response.url))
    
    def get_current_weather(self, latitude: float, longitude: float) -> Dict:
        """
        Get current weather data for given coordinates.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
        
        Returns:
            Dictionary with current weather data
            
        Raises:
            WeatherAPIError: For API errors
        """
        # Prepare query parameters for weather API
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "timezone": "auto"
        }
        
        try:
            print(f"  Making weather request for coordinates: {latitude}, {longitude}")
            print(f" Request URL: {self.weather_url}")
            print(f" Parameters: {params}")
            
            # Make the HTTP request
            response = self.session.get(
                self.weather_url,
                params=params,
                timeout=10
            )
            
            print(f" Response Status Code: {response.status_code}")
            print(f" Final URL: {response.url}")
            
            # Handle HTTP errors
            if not response.ok:
                raise WeatherAPIError(
                    f"Weather API request failed: {response.reason}",
                    status_code=response.status_code,
                    url=str(response.url)
                )
            
            # Parse JSON response
            data = response.json()
            print(f" Raw Response: {json.dumps(data, indent=2)}")
            
            # Extract current weather data
            current = data.get("current_weather", {})
            result = {
                "temperature_c": current.get("temperature"),
                "windspeed_kmh": current.get("windspeed"),
                "observation_time": current.get("time"),
                "weather_code": current.get("weathercode")
            }
            
            print(f" Successfully retrieved weather data: {result}")
            return result
            
        except requests.exceptions.Timeout:
            raise WeatherAPIError("Weather request timed out", url=self.weather_url)
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Weather connection failed", url=self.weather_url)
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"Weather request failed: {e}", url=self.weather_url)
        except json.JSONDecodeError:
            raise WeatherAPIError("Invalid weather JSON response", url=str(response.url))


```

