# AI Travel Planner

An intelligent travel planning application that uses AI to generate personalized travel itineraries based on user preferences.

## Features

- AI-powered travel research and planning
- Personalized itinerary generation
- Real-time weather and attraction information
- Budget-aware recommendations
- Interactive user interface
- Exportable travel plans
- User feedback system

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Start the application:
```bash
streamlit run src/app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Enter your travel preferences:
   - Destination
   - Trip duration
   - Interests
   - Budget range
   - Travel pace

4. Click "Generate Travel Plan" to create your personalized itinerary

5. Download or share your travel plan

## Project Structure

```
travel_planner/
├── .env                    # Environment variables
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
├── src/
│   ├── __init__.py
│   ├── agents/           # AI agents for research and planning
│   ├── utils/           # Utility functions
│   └── app.py           # Main Streamlit application
└── tests/               # Test files
```

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