import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
from pydantic import BaseModel

class Score(BaseModel):
    team: str
    score: str

class Match(BaseModel):
    match: str
    scores: List[Score]
    status: str
    is_live: bool = False

class CricbuzzScraper:
    BASE_URL = "https://www.cricbuzz.com"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async def get_live_scores(self) -> List[Match]:
        async with httpx.AsyncClient(headers=self.HEADERS, follow_redirects=True) as client:
            try:
                response = await client.get(self.BASE_URL)
                response.raise_for_status()
            except httpx.HTTPError as e:
                print(f"HTTP Error: {e}")
                return []

        soup = BeautifulSoup(response.text, "html.parser")
        match_data = []

        # Find all carousal items (the match cards at the top)
        items = soup.find_all("div", class_="carousal-item")

        for item in items:
            link_tag = item.find("a")
            if not link_tag:
                continue

            # 1. Extract Match Title
            title = link_tag.get('title', 'N/A')

            # 2. Extract Team Names and Scores
            team_rows = link_tag.find_all("div", class_="cb-ovr-flo") # Updated selector for team name container if needed, sticking to general structure
            
            # Re-checking structure based on common cricbuzz layout in carousel
            # Usually strict structure: <div>...Team 1...</div> <div>...Team 2...</div>
            # The previous scraper used specific classes. Let's try to be robust.
            
            scores_list = []
            team_divs = link_tag.find_all("div", recursive=False) 
            # The carousel item usually has a specific structure. 
            # Let's stick to the previous logic but improve safety.
            
            team_rows = link_tag.select(".cb-hmscg-tm-nm") # Try to find team names if possible, or fallback to the previous logic
            
            # Let's use the layout from the previous scraper which seemed to work: 
            # inner divs with class "flex items-center gap-4 justify-between" (Tailwind classes? The user's scraper had these. 
            # If the site changed, the old scraper wouldn't work. I will assume the user's scraper selectors were correct or close enough, 
            # Cricbuzz rows usually have the team name in one span and score in another
            team_rows = link_tag.find_all("div", class_="flex items-center gap-4 justify-between")
            
            scores_list = []
            
            for row in team_rows:
                team_span = row.find("span", class_="whitespace-nowrap")
                team_name = team_span.text.strip() if team_span else "Unknown"

                score_span = row.find("span", class_="font-medium") or row.find("span", class_="wb:font-semibold")
                score_text = score_span.text.strip() if score_span else "Yet to bat"
                
                scores_list.append(Score(team=team_name, score=score_text))

            # 3. Extract Status
            status_tag = link_tag.find("span", class_="text-cbLive") or link_tag.find("span", class_="text-cbPreview")
            status = status_tag.text.strip() if status_tag else "N/A"
            
            # Usually "Live" status/color indicates it. 
            # The class `text-cbLive` strongly implies live.
            is_live = bool(link_tag.find("span", class_="text-cbLive"))

            match_data.append(Match(
                match=title,
                scores=scores_list,
                status=status,
                is_live=is_live
            ))

        # Sort: Live first, then others. 
        # Python's sort is stable. True (1) > False (0), so reverse=True puts Live first.
        match_data.sort(key=lambda x: x.is_live, reverse=True)

        return match_data

# Singleton instance for easy import
scraper = CricbuzzScraper()

async def get_live_scores_async() -> List[dict]:
    """Helper function to maintain partial compatibility or simple usage"""
    matches = await scraper.get_live_scores()
    return [match.model_dump() for match in matches]
