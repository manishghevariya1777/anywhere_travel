import streamlit as st
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from agents.search_agent import search_destination_info
from agents.planning_agent import generate_plan
from utils.markdown_utils import clean_markdown, sanitize_filename
from utils.validation import validate_inputs
from utils.weather_currency import get_weather_forecast, convert_currency, get_currency_symbol
from utils.cost_estimation import estimate_total_cost

# Load environment variables
load_dotenv()

def validate_api_keys():
    required_keys = {
        "OPENAI_API_KEY": "OpenAI API key is required for trip planning",
        "OPENWEATHER_API_KEY": "OpenWeather API key is required for weather information",
        "EXCHANGERATES_API_KEY": "ExchangeRates API key is required for currency conversion"
    }
    
    missing_keys = []
    for key, message in required_keys.items():
        if not os.getenv(key):
            missing_keys.append(message)
    
    return missing_keys

# Utility: Map destination to currency code (simple version)
def get_currency_code(destination):
    mapping = {
        'japan': 'JPY', 'tokyo': 'JPY', 'osaka': 'JPY',
        'france': 'EUR', 'paris': 'EUR',
        'uk': 'GBP', 'london': 'GBP',
        'united kingdom': 'GBP',
        'usa': 'USD', 'united states': 'USD', 'new york': 'USD', 'los angeles': 'USD',
        'india': 'INR', 'delhi': 'INR', 'mumbai': 'INR',
        'china': 'CNY', 'beijing': 'CNY', 'shanghai': 'CNY',
        'australia': 'AUD', 'sydney': 'AUD',
        'canada': 'CAD', 'toronto': 'CAD',
    }
    dest = destination.lower().strip()
    for key in mapping:
        if key in dest:
            return mapping[key]
    return 'USD'  # fallback

def main():
    # Validate API keys
    missing_keys = validate_api_keys()
    if missing_keys:
        st.error("Missing required API keys. Please set the following environment variables:")
        for message in missing_keys:
            st.error(f"- {message}")
        return

    # Set page config with custom theme
    st.set_page_config(
        page_title="Anywhere Travel",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for modern UI/UX
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        html, body, .stApp {
            background: linear-gradient(to bottom, #eaf3fa 0%, #fafdff 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        .main-header {
            width: 100vw;
            background: rgba(255,255,255,0.97);
            border-bottom: 2px solid #e0e7ef;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 2rem 1rem 2rem;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 100;
            height: 8rem;
        }
        .main-header .logo {
            font-size: 1.1rem;
            font-weight: 900;
            color: #2563eb;
            letter-spacing: -1px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .main-header .nav {
            display: flex;
            gap: 2rem;
        }
        .main-header .nav a {
            color: #2563eb;
            font-weight: 600;
            text-decoration: none;
            font-size: 1rem;
            transition: color 0.2s;
        }
        .main-header .nav a:hover {
            color: #059669;
        }
        .main-content {
            padding-top: 8rem;
            margin: 0;
            padding-bottom: 0;
        }
        .main-content > img {
            display: block;
            width: 100%;
            max-width: 700px;
            margin: 0.5rem auto 2rem auto;
            border-radius: 1.5rem;
            box-shadow: 0 4px 24px rgba(0,0,0,0.10);
            object-fit: cover;
            max-height: 320px;
        }
        .center-card {
            background: #fff;
            border: none;
            border-radius: 1.5rem;
            box-shadow: none;
            max-width: 500px;
            margin: 2rem auto;
            padding: 0.7rem 1rem 1rem 1rem;
            display: flex;
            flex-direction: column;
        }
        .center-card h2 {
            color: #23406e;
            font-size: 1.7rem;
            text-align: center;
            background: #fff;
            border-radius: 1rem;
            padding: 0.5rem 1.5rem;
            margin: 0 auto 0.7rem auto;
            display: inline-block;
            box-shadow: none;
        }
        .heading-box {
            display: flex;
            justify-content: center;
        }
        .section-header {
            background: #23406e;
            color: #fff;
            font-weight: 800;
            font-size: 1.15rem;
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin-bottom: 0.3rem;
            margin-top: 0;
            padding: 0.5rem 1rem;
            border-radius: 0.7rem 0.7rem 0 0;
            border-left: 6px solid #1ecbe1;
            box-shadow: none;
        }
        .section-details, .section-duration, .section-preferences, .section-pace, .section-submit {
            background: #fafdff;
            border-radius: 1.3rem;
            padding: 0.5rem 0.7rem 0.7rem 0.7rem;
            margin-bottom: 0.7rem;
            box-shadow: none;
            border: none;
        }
        .form-grid {
            gap: 0.7rem;
        }
        .form-label {
            font-weight: 600;
            color: #2563eb;
            margin-bottom: 0.3rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.1rem;
        }
        .stForm label[data-testid="stWidgetLabel"], .stForm label {
            color: #23406e !important;
        }
        .form-input {
            width: 100%;
        }
        .form-input input, .form-input select {
            width: 100%;
            border: 1.5px solid #d1d5db;
            border-radius: 0.75rem;
            padding: 1rem 1.2rem;
            font-size: 1.1rem;
            outline: none;
            transition: border 0.2s;
        }
        .form-input input:focus, .form-input select:focus {
            border: 1.5px solid #1ecbe1;
            box-shadow: none;
        }
        .submit-btn {
            background: linear-gradient(90deg, #1ecbe1 0%, #23406e 100%);
            color: #fff;
            font-weight: 800;
            font-size: 1.22rem;
            border: none;
            border-radius: 0.9rem;
            padding: 1.1rem 0;
            margin-top: 2rem;
            margin-bottom: 0.5rem;
            box-shadow: none;
            transition: background 0.2s, transform 0.1s;
        }
        .submit-btn:hover {
            background: linear-gradient(90deg, #23406e 0%, #1ecbe1 100%);
            color: #fff;
        }
        .footer {
            width: 100vw;
            background: #23406e;
            color: #fff;
            border-top: none;
            padding: 1.5rem 0 1rem 0;
            text-align: center;
            position: relative;
            left: 0;
            bottom: 0;
            z-index: 100;
            font-size: 1.05rem;
        }
        @media (max-width: 700px) {
            .footer { position: static; }
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div class='main-header'>
            <div class='logo'>
                <span>✈️</span> Anywhere Travel
            </div>
            <nav class='nav'>
                <a href='#'>Home</a>
                <a href='#'>Login</a>
            </nav>
        </div>
    """, unsafe_allow_html=True)

    # Main Content Wrapper and Banner Image together (no unnecessary divs)
    st.markdown("""<div class='main-content'><img src='https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=900&q=80' alt='Travel Banner' style='display:block;width:100%;max-width:700px;margin:0 auto 2.5rem auto;border-radius:1.5rem;box-shadow:0 4px 24px rgba(0,0,0,0.10);object-fit:cover;max-height:320px;margin-top:0;'></div>""", unsafe_allow_html=True)

    # Centered Card with Form
    st.markdown("<div class='center-card'>\n<div class='heading-box'><h2>Plan Your Dream Trip</h2></div>", unsafe_allow_html=True)
    with st.form(key="travel_form"):
        # --- Trip Details ---
        st.markdown("<div class='section-details'><div class='section-header'>✈️ Trip Details</div><div class='form-grid'>", unsafe_allow_html=True)
        origin = st.text_input(
            label="✈️ Flying From",
            placeholder="Enter city or airport",
            key="origin_input"
        )
        destination = st.text_input(
            label="✈️ Flying To",
            placeholder="Enter city or airport",
            key="destination_input"
        )
        st.markdown("</div></div>", unsafe_allow_html=True)

        # --- Duration ---
        st.markdown("<div class='section-duration'><div class='section-header'>⏱️ Duration</div><div class='form-grid'>", unsafe_allow_html=True)
        start_date = st.date_input(
            label="⏱️ Start Date",
            min_value=datetime.now() + timedelta(days=1),
            value=datetime.now() + timedelta(days=30),
            key="start_date_input"
        )
        duration = st.slider(
            label="📅 Number of Days",
            min_value=1,
            max_value=30,
            value=7,
            key="duration_slider"
        )
        st.markdown("</div></div>", unsafe_allow_html=True)

        # --- Preferences ---
        st.markdown("<div class='section-preferences'><div class='section-header'>🎯 Preferences</div><div class='form-grid'>", unsafe_allow_html=True)
        interests = st.multiselect(
            label="🎯 Interests",
            options=["Culture", "Food", "Shopping", "Nature", "Nightlife", "History", "Adventure", "Relaxation"],
            default=[],
            key="interests_multi",
            help="Select what you enjoy most"
        )
        budget = st.selectbox(
            label="💰 Budget Level",
            options=["Budget", "Mid-Range", "Luxury"],
            index=1,
            key="budget_select",
            help="Your budget range"
        )
        st.markdown("</div></div>", unsafe_allow_html=True)

        # --- Pace ---
        st.markdown("<div class='section-pace'><div class='section-header'>🏃 Travel Pace</div>", unsafe_allow_html=True)
        pace = st.radio(
            label="",
            options=["Relaxed", "Moderate", "Packed"],
            index=0,
            key="pace_radio",
            help="How busy do you want your trip? (Relaxed, Moderate, or Packed)"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        submit_button = st.form_submit_button(
            label="Plan My Trip"
        )
    st.markdown("</div>", unsafe_allow_html=True)  # Close center-card
    st.markdown("</div>", unsafe_allow_html=True)  # Close main-content

    # Footer
    st.markdown("""
        <div class='footer'>
            © 2025 Anywhere Travel &nbsp;|&nbsp; Making travel planning effortless ✈️
        </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if 'last_plan' not in st.session_state:
        st.session_state.last_plan = None
    if 'last_destination' not in st.session_state:
        st.session_state.last_destination = None

    # Results Section
    if submit_button:
        # Validate that required fields are filled
        if not origin or not destination:
            st.error("Please enter both origin and destination cities.")
            return
            
        preferences = {
            "interests": interests,
            "budget": budget,
            "pace": pace
        }
        
        # Get local currency code and symbol
        currency_code = get_currency_code(destination)
        currency_symbol = get_currency_symbol(currency_code)
        preferences["currency"] = currency_symbol
        
        # Validate inputs
        is_valid, error_msg = validate_inputs(origin, destination, duration, preferences)
        if not is_valid:
            st.error(error_msg)
            return
        
        with st.spinner("🔍 Creating your personalized travel plan..."):
            # Search phase
            search_data = search_destination_info(destination)
            
            # Get weather information
            weather_data = get_weather_forecast(destination, days=duration)
            if weather_data:
                weather_info = "\n\n### Weather Forecast\n"
                for day in weather_data["forecast"]:
                    weather_info += f"- {day['date']}: {day['temp']}°C, {day['description']}\n"
                search_data += weather_info
            
            # Get cost estimation in USD
            cost_estimation = estimate_total_cost(origin, destination, duration, budget)
            # Convert costs to local currency if not USD
            def conv(amount):
                if currency_code == 'USD':
                    return amount
                converted = convert_currency(amount, 'USD', currency_code)
                return converted if converted is not None else amount
            cost_info = f"\n\n### Cost Estimation (in {currency_symbol} and $)\n"
            cost_info += f"- Flight Cost: {currency_symbol}{conv(cost_estimation['flight_cost']):.2f} (${'{:.2f}'.format(cost_estimation['flight_cost'])})\n"
            cost_info += f"- Hotel Cost: {currency_symbol}{conv(cost_estimation['hotel_cost']):.2f} (${'{:.2f}'.format(cost_estimation['hotel_cost'])})\n"
            cost_info += f"- Daily Expenses: {currency_symbol}{conv(cost_estimation['daily_expenses']):.2f} (${'{:.2f}'.format(cost_estimation['daily_expenses'])})\n"
            cost_info += f"- Daily Budget: {currency_symbol}{conv(cost_estimation['daily_budget']):.2f} (${'{:.2f}'.format(cost_estimation['daily_budget'])})\n"
            cost_info += f"- Total Cost: {currency_symbol}{conv(cost_estimation['total_cost']):.2f} (${'{:.2f}'.format(cost_estimation['total_cost'])})\n"
            search_data += cost_info
            
            # Planning phase
            # Update the planning prompt to mention the correct currencies
            preferences['currency_code'] = currency_code
            result = generate_plan(destination, duration, preferences, search_data)
            
            if result.startswith("Error:"):
                st.error(result)
            else:
                # Clean and format the markdown
                cleaned_result = clean_markdown(result)
                
                st.markdown("## ✈️ Your Travel Plan")
                st.markdown(cleaned_result, unsafe_allow_html=True)
                
                # Store the last plan in session state
                st.session_state.last_plan = cleaned_result
                st.session_state.last_destination = destination

    # Download button
    if st.session_state.last_plan:
        sanitized_destination = sanitize_filename(st.session_state.last_destination)
        st.download_button(
            label="Download Travel Plan",
            data=st.session_state.last_plan,
            file_name=f"{sanitized_destination}_travel_plan_2025.md",
            mime="text/markdown",
            use_container_width=True
        )

if __name__ == "__main__":
    main() 