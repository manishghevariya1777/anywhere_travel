import os
import csv
from datetime import datetime
import streamlit as st

def validate_inputs(origin: str, destination: str, duration: int, preferences: dict) -> tuple[bool, str]:
    """
    Validate user inputs for travel planning.
    
    Args:
        origin: The starting city
        destination: The travel destination
        duration: Number of days for the trip
        preferences: User preferences dictionary
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not origin or not origin.strip():
        return False, "Please enter a valid starting city."
    
    if not destination or not destination.strip():
        return False, "Please enter a valid destination."
    
    if origin.lower() == destination.lower():
        return False, "Origin and destination cannot be the same."
    
    if duration < 1:
        return False, "Duration must be at least 1 day."
    
    if duration > 30:
        return False, "Duration cannot exceed 30 days."
    
    if not preferences or not all(key in preferences for key in ["interests", "budget", "pace"]):
        return False, "Invalid preferences format."
    
    if not preferences["interests"]:
        return False, "Please select at least one interest."
    
    return True, ""

def validate_feedback(rating: int, comments: str) -> tuple[bool, str]:
    """
    Validate feedback data before saving.
    
    Args:
        rating: User rating (1-5)
        comments: User comments
        
    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return False, "Invalid rating value"
    if not isinstance(comments, str) or len(comments.strip()) == 0:
        return False, "Comments cannot be empty"
    return True, ""

def save_feedback(timestamp: str, destination: str, duration: int, rating: int, comments: str) -> bool:
    """
    Save user feedback to a CSV file.
    
    Args:
        timestamp: Feedback timestamp
        destination: Travel destination
        duration: Trip duration
        rating: User rating
        comments: User comments
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        # Validate feedback data
        is_valid, error_msg = validate_feedback(rating, comments)
        if not is_valid:
            st.error(f"Invalid feedback: {error_msg}")
            return False
        
        # Create feedback directory if it doesn't exist
        os.makedirs("feedback", exist_ok=True)
        
        # Use a structured filename with date
        filename = f"feedback/feedback_{datetime.now().strftime('%Y%m')}.csv"
        
        # Check if file exists to determine if we need headers
        file_exists = os.path.isfile(filename)
        
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Destination", "Duration", "Rating", "Comments"])
            writer.writerow([timestamp, destination, duration, rating, comments])
        return True
    except Exception as e:
        st.error(f"Error saving feedback: {str(e)}")
        return False 