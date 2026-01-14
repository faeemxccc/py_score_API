# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_live_scores
 # Import your function

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all websites to access your API
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/live-matches")
def read_scores():
    # Call your scraper
    data = get_live_scores()
    
    # Return the data. FastAPI converts this to JSON automatically!
    return {
        "count": len(data),
        "matches": data
    }