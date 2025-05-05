import requests
from typing import Dict, List, Optional
import os
from datetime import datetime, timedelta

def get_place_coordinates(place: str) -> Optional[Dict[str, float]]:
    """
    Get coordinates (latitude, longitude) for a place using OpenStreetMap Nominatim API.
    
    Args:
        place: Name of the place
        
    Returns:
        Dict: Dictionary with 'lat' and 'lon' keys or None if error
    """
    try:
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": place,
            "format": "json",
            "limit": 1
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    "lat": float(data[0]["lat"]),
                    "lon": float(data[0]["lon"])
                }
    except Exception as e:
        print(f"Error getting coordinates: {str(e)}")
    return None

def get_nearby_places(lat: float, lon: float, radius: int = 1000) -> Optional[List[Dict]]:
    """
    Get nearby places of interest using OpenStreetMap Overpass API.
    
    Args:
        lat: Latitude
        lon: Longitude
        radius: Search radius in meters (default 1000m)
        
    Returns:
        List[Dict]: List of nearby places or None if error
    """
    try:
        query = f"""
        [out:json];
        (
          node["tourism"](around:{radius},{lat},{lon});
          node["amenity"](around:{radius},{lat},{lon});
        );
        out body;
        """
        
        response = requests.post(
            "https://overpass-api.de/api/interpreter",
            data=query
        )
        
        if response.status_code == 200:
            data = response.json()
            places = []
            for element in data.get("elements", []):
                if "tags" in element:
                    places.append({
                        "name": element["tags"].get("name", "Unnamed Place"),
                        "type": element["tags"].get("tourism") or element["tags"].get("amenity"),
                        "lat": element["lat"],
                        "lon": element["lon"]
                    })
            return places
    except Exception as e:
        print(f"Error getting nearby places: {str(e)}")
    return None

def generate_travel_checklist(
    destination: str,
    duration: int,
    activities: List[str],
    season: str
) -> Dict[str, List[str]]:
    """
    Generate a comprehensive travel checklist based on destination and trip details.
    
    Args:
        destination: Travel destination
        duration: Trip duration in days
        activities: List of planned activities
        season: Travel season
        
    Returns:
        Dict[str, List[str]]: Organized checklist by category
    """
    # Base checklist items
    checklist = {
        "Documents": [
            "Passport/ID",
            "Travel insurance",
            "Flight/train tickets",
            "Hotel reservations",
            "Emergency contacts"
        ],
        "Electronics": [
            "Phone and charger",
            "Power bank",
            "Adapter/converter",
            "Camera (if needed)"
        ],
        "Clothing": [],
        "Toiletries": [
            "Toothbrush and toothpaste",
            "Deodorant",
            "Shampoo and conditioner",
            "Sunscreen",
            "Basic first aid kit"
        ],
        "Miscellaneous": [
            "Water bottle",
            "Snacks",
            "Travel pillow",
            "Earplugs",
            "Eye mask"
        ]
    }
    
    # Add season-specific clothing
    if season.lower() in ["summer", "spring"]:
        checklist["Clothing"].extend([
            "Light clothing",
            "Sunglasses",
            "Hat",
            "Swimsuit",
            "Sandals"
        ])
    elif season.lower() in ["winter", "fall"]:
        checklist["Clothing"].extend([
            "Warm clothing",
            "Jacket",
            "Gloves",
            "Scarf",
            "Boots"
        ])
    
    # Add activity-specific items
    if "hiking" in [a.lower() for a in activities]:
        checklist["Miscellaneous"].extend([
            "Hiking shoes",
            "Backpack",
            "Waterproof jacket",
            "Map/compass"
        ])
    
    if "beach" in [a.lower() for a in activities]:
        checklist["Miscellaneous"].extend([
            "Beach towel",
            "Sunglasses",
            "Beach bag",
            "Waterproof phone case"
        ])
    
    # Add duration-specific items
    if duration > 7:
        checklist["Toiletries"].extend([
            "Laundry detergent",
            "Extra toiletries"
        ])
    
    return checklist 