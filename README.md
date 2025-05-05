# Anywhere Travel – Modern Streamlit Travel Planner

Anywhere Travel is a modern, user-friendly travel planning web app built with Streamlit. It features a beautiful, responsive UI with a light navy, white, and ocean-inspired color palette. Users can plan trips, select preferences, and download personalized itineraries.

## Features

Modern, Responsive UI: Clean cards, beautiful color theme, and mobile-friendly layout.
Fixed Header & Footer: Professional navigation and branding.
Banner Image: Sets the mood for travel inspiration.
Multi-Section Form: Collects trip details, duration, preferences, and pace.
Smart Validation: Ensures all required fields are filled.
Personalized Plan Generation: Integrates with AI agents and APIs for destination info, weather, and cost estimation.
Downloadable Itinerary: Users can download their plan as a Markdown file.
Accessible & User-Friendly: Visible labels, color contrast, and keyboard navigation.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner
```

2. Install Dependencies
Create a requirements.txt with:
streamlit
python-dotenv

3. Set Environment Variables
Create a .env file in the project root with your API keys:
OPENAI_API_KEY=your_openai_key
OPENWEATHER_API_KEY=your_openweather_key
EXCHANGERATES_API_KEY=your_exchangerates_key

4. Run the App
streamlit run app.py


## Project Structure

.
├── app.py
├── agents/
│   ├── search_agent.py
│   └── planning_agent.py
├── utils/
│   ├── markdown_utils.py
│   ├── validation.py
│   ├── weather_currency.py
│   ├── cost_estimation.py
│   └── storage.py
├── requirements.txt
├── .env.example
└── README.md

## Security

- Never commit your `.env` file or expose your API keys
- Keep your dependencies updated
- Use environment variables for sensitive information

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For support, please open an issue in the GitHub repository. 
