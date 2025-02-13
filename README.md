# Scraper Tool

This is a scraping tool built with FastAPI that automates the process of scraping product information (name, price, and image) from the Dentalstall website. It supports optional settings for limiting the number of pages to scrape and using a proxy for requests. The tool uses an object‐oriented approach with abstractions for storage and notifications, and it features a simple caching mechanism and retry logic.

## Project Structure

scraper_tool/
├── main.py                # FastAPI application entry point
├── config.py              # Configuration (token, retry settings, base URL, etc.)
├── requirements.txt       # Dependencies
├── README.md              # Read me file
├── api/                   # API-related code
│   ├── auth.py            # Token-based authentication dependency
│   └── routes.py          # API route definitions
├── models/                # Pydantic models
│   ├── product.py         # Product model
│   └── settings.py        # Scraper settings model
└── scraper/               # Scraping logic and helpers
    ├── scraper.py         # Scraping implementation with retry and pagination
    ├── storage.py         # Storage abstraction (JSON file by default)
    ├── cache.py           # Simple in-memory cache
    └── notifier.py        # Notification abstraction (currently prints to console)



## Setup & Usage

1. **Install Dependencies:**

   pip install -r requirements.txt

2. **Run the Application:**

   uvicorn main:app --reload

3. **Test the API Endpoint:**

   Endpoint: POST http://localhost:8000/scrape
   Headers: Authorization: Bearer <your_token>  <!-- my_secure_token_123 -->
