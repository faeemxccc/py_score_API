# Live Cricket Scores API

A simple web scraping project that fetches live cricket match scores from Cricbuzz and serves them via a FastAPI REST API.

## Description

This project scrapes live cricket match data from the Cricbuzz website using BeautifulSoup and requests. The scraped data includes match titles, team scores, and current match status. The data is then exposed through a FastAPI web server with CORS enabled for easy integration with web applications.

**Note:** This project is for educational purposes only. Web scraping may violate the terms of service of the target website. Always ensure compliance with legal and ethical guidelines when scraping websites.

## Features

- Scrapes live cricket match data from Cricbuzz
- Extracts match titles, team names, scores, and status
- Serves data via REST API with FastAPI
- CORS enabled for cross-origin requests
- Lightweight and easy to deploy

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd webscrap
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   ```

## Usage

Run the FastAPI server:

```bash
fastapi dev main.py
```

The API will be available at `http://localhost:8000`.

### API Endpoints

- `GET /live-matches`: Returns a JSON object with live cricket match data.

Example response:
```json
{
  "count": 2,
  "matches": [
    {
      "match": "IND vs NZ",
      "scores": [
        {"team": "IND", "score": "284-7 (50)"},
        {"team": "NZ", "score": "Yet to bat"}
      ],
      "status": "NZ need 239 runs"
    }
  ]
}
```

You can also access the interactive API documentation at `http://localhost:8000/docs`.

## Dependencies

- `beautifulsoup4`: For HTML parsing
- `fastapi[standard]`: For the web API framework
- `requests`: For HTTP requests

## Development

- Python 3.13+
- Uses uv for dependency management
- Virtual environment included

## License

This project is open-source. Please check the terms of service of Cricbuzz before using this scraper in production.
