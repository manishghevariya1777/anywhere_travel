from duckduckgo_search import DDGS
import streamlit as st
from typing import List, Dict

def search_destination(query: str, max_results: int = 5) -> List[Dict]:
    """Search for destination information using DuckDuckGo."""
    if not query or not isinstance(query, str):
        st.error("Invalid search query provided")
        return []
        
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            if not results:
                st.warning("No search results found. Try a different search query.")
            return results
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return []

def search_destination_info(destination: str) -> str:
    """
    Search for destination information and return gathered data.
    
    Args:
        destination: The destination to search for
        
    Returns:
        str: Search data or error message
    """
    if not destination or not isinstance(destination, str):
        return "Error: Invalid destination provided."
        
    try:
        search_prompt = f"""
        Search for 2025 travel data for {destination}. Include:
        - Best time to visit (weather, events)
        - Popular attractions and activities
        - Hotel options in different price ranges
        - Local transportation info
        - Typical travel costs
        """
        
        with st.spinner("Searching destination information..."):
            results = search_destination(search_prompt)
            
            if not results:
                return "Error: No search data found for the destination."
                
            # Format the results
            search_data = "\n\n".join([
                f"### {result['title']}\n{result['body']}"
                for result in results
            ])
            
            return search_data
            
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return "Limited information available due to search error." 