import json
import os
from datetime import datetime
from typing import Dict, List, Optional

def save_travel_plan(plan_data: Dict) -> bool:
    """
    Save a travel plan to the plans directory.
    
    Args:
        plan_data: Dictionary containing plan information
        
    Returns:
        bool: True if saved successfully
    """
    try:
        # Create plans directory if it doesn't exist
        os.makedirs("plans", exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"plans/plan_{timestamp}.json"
        
        # Save plan data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(plan_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving plan: {str(e)}")
        return False

def load_travel_plans() -> List[Dict]:
    """
    Load all saved travel plans.
    
    Returns:
        List[Dict]: List of travel plans
    """
    plans = []
    try:
        if not os.path.exists("plans"):
            return plans
            
        for filename in os.listdir("plans"):
            if filename.endswith(".json"):
                with open(os.path.join("plans", filename), "r", encoding="utf-8") as f:
                    plan_data = json.load(f)
                    plans.append(plan_data)
    except Exception as e:
        print(f"Error loading plans: {str(e)}")
    return plans

def delete_travel_plan(plan_id: str) -> bool:
    """
    Delete a saved travel plan.
    
    Args:
        plan_id: The ID of the plan to delete
        
    Returns:
        bool: True if deleted successfully
    """
    try:
        filename = f"plans/plan_{plan_id}.json"
        if os.path.exists(filename):
            os.remove(filename)
            return True
    except Exception as e:
        print(f"Error deleting plan: {str(e)}")
    return False 