# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_live_scores_async

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all websites to access your API
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live-matches")
async def read_scores():
    # Call your scraper asynchronously
    data = await get_live_scores_async()
    
    return {
        "count": len(data),
        "matches": data
    }