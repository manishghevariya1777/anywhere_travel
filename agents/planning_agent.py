from openai import OpenAI
import streamlit as st
import os
from typing import Dict, Optional

def get_openai_client() -> Optional[OpenAI]:
    """Initialize and return the OpenAI client."""
    if "OPENAI_API_KEY" not in os.environ:
        st.error("OpenAI API key not found in environment variables.")
        return None
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def validate_inputs(destination: str, duration: int, preferences: Dict, search_data: str) -> tuple[bool, str]:
    """Validate input parameters for plan generation."""
    if not destination or not isinstance(destination, str):
        return False, "Invalid destination provided"
        
    if not isinstance(duration, int) or duration < 1 or duration > 30:
        return False, "Duration must be between 1 and 30 days"
        
    if not preferences or not isinstance(preferences, dict):
        return False, "Invalid preferences provided"
        
    if not search_data or not isinstance(search_data, str):
        return False, "Invalid search data provided"
        
    return True, ""

def generate_plan(destination: str, duration: int, preferences: Dict, search_data: str) -> str:
    """
    Generate a travel plan based on search data and user preferences.
    
    Args:
        destination: The travel destination
        duration: Number of days for the trip
        preferences: User preferences dictionary
        search_data: Search data from the search agent
        
    Returns:
        str: Generated travel plan or error message
    """
    # Validate inputs
    is_valid, error_msg = validate_inputs(destination, duration, preferences, search_data)
    if not is_valid:
        return f"Error: {error_msg}"
        
    try:
        client = get_openai_client()
        if not client:
            return "Error: Unable to initialize OpenAI client. Please check your API key configuration."
            
        planning_prompt = f"""
        Create a detailed travel plan for {destination} for {duration} days in 2025.
        User preferences: {preferences}.
        Incorporate this search data: {search_data}.
        Include:
        - Best time to visit
        - Top attractions and activities tailored to preferences
        - Recommended hotels matching budget
        - Local transportation options and tips
        - Estimated daily budget breakdown in JPY and USD (1 USD = 154 JPY)
        Format in clean Markdown. Ensure all sections are complete and tailored to preferences.
        """
        
        with st.spinner("Generating your personalized travel plan..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional travel planner. Generate detailed, personalized travel plans in Markdown format."},
                    {"role": "user", "content": planning_prompt}
                ],
                max_tokens=2500,
                temperature=0.7
            )
            
            if not response.choices:
                return "Error: No response generated from OpenAI."
                
            plan = response.choices[0].message.content
            if not plan or len(plan.strip()) < 100:
                return "Error: Generated plan is too short or empty. Please try again."
                
            return plan
            
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg.lower():
            return "Error: Invalid OpenAI API key. Please check your configuration."
        elif "rate limit" in error_msg.lower():
            return "Error: OpenAI API rate limit exceeded. Please try again later."
        else:
            return f"Error generating plan: {error_msg}" 