import requests
from typing import Dict, Optional
import os

def get_flight_cost(origin: str, destination: str) -> Optional[float]:
    """
    Get estimated flight cost using a flight API.
    This is a mock implementation - in production, you would use a real flight API.
    """
    # Mock flight costs (in USD)
    mock_costs = {
        "new york": {"london": 800, "tokyo": 1200, "paris": 900},
        "london": {"new york": 800, "tokyo": 1000, "paris": 200},
        "tokyo": {"new york": 1200, "london": 1000, "paris": 1100},
        "paris": {"new york": 900, "london": 200, "tokyo": 1100}
    }
    
    origin = origin.lower()
    destination = destination.lower()
    
    if origin in mock_costs and destination in mock_costs[origin]:
        return mock_costs[origin][destination]
    return 1000  # Default cost if route not found

def get_hotel_cost(destination: str, duration: int, budget_level: str) -> float:
    """
    Get estimated hotel cost based on destination and budget level.
    """
    # Mock hotel costs per night (in USD)
    mock_costs = {
        "new york": {"budget": 100, "mid-range": 200, "luxury": 400},
        "london": {"budget": 80, "mid-range": 160, "luxury": 320},
        "tokyo": {"budget": 70, "mid-range": 140, "luxury": 280},
        "paris": {"budget": 90, "mid-range": 180, "luxury": 360}
    }
    
    destination = destination.lower()
    budget_level = budget_level.lower()
    
    if destination in mock_costs and budget_level in mock_costs[destination]:
        return mock_costs[destination][budget_level] * duration
    return 150 * duration  # Default cost if destination not found

def get_daily_expenses(destination: str, budget_level: str) -> float:
    """
    Get estimated daily expenses based on destination and budget level.
    """
    # Mock daily expenses (in USD)
    mock_costs = {
        "new york": {"budget": 50, "mid-range": 100, "luxury": 200},
        "london": {"budget": 40, "mid-range": 80, "luxury": 160},
        "tokyo": {"budget": 35, "mid-range": 70, "luxury": 140},
        "paris": {"budget": 45, "mid-range": 90, "luxury": 180}
    }
    
    destination = destination.lower()
    budget_level = budget_level.lower()
    
    if destination in mock_costs and budget_level in mock_costs[destination]:
        return mock_costs[destination][budget_level]
    return 75  # Default cost if destination not found

def estimate_total_cost(origin: str, destination: str, duration: int, budget_level: str) -> Dict[str, float]:
    """
    Estimate total trip cost including flights, accommodation, and daily expenses.
    """
    flight_cost = get_flight_cost(origin, destination)
    hotel_cost = get_hotel_cost(destination, duration, budget_level)
    daily_expenses = get_daily_expenses(destination, budget_level) * duration
    
    total_cost = flight_cost + hotel_cost + daily_expenses
    
    # Calculate daily budget
    daily_budget = (hotel_cost + daily_expenses) / duration
    
    return {
        "flight_cost": flight_cost,
        "hotel_cost": hotel_cost,
        "daily_expenses": daily_expenses,
        "total_cost": total_cost,
        "daily_budget": daily_budget
    } 