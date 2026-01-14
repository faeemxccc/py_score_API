# scraper.py
from bs4 import BeautifulSoup
import requests
def get_live_scores():
    url = "https://www.cricbuzz.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    match_data = []
    # Find all carousal items (the match cards at the top)
    items = soup.find_all("div", class_="carousal-item")
    
    for item in items:
        # Each card is a link <a>
        link_tag = item.find("a")
        if not link_tag:
            continue

        # 1. Extract the Match Title (e.g., "IND vs NZ")
        title = link_tag.get('title', 'N/A')

        # 2. Extract Team Names and Scores
        # Cricbuzz rows usually have the team name in one span and score in another
        team_rows = link_tag.find_all("div", class_="flex items-center gap-4 justify-between")
        
        scores = []
        for row in team_rows:
            # The team name (e.g., "IND")
            team_name = row.find("span", class_="whitespace-nowrap").text if row.find("span") else "Unknown"
            # The score (e.g., "284-7 (50)")
            score_val = row.find("span", class_="font-medium") or row.find("span", class_="wb:font-semibold")
            score_text = score_val.text.strip() if score_val else "Yet to bat"
            
            scores.append({"team": team_name, "score": score_text})

        # 3. Extract the Match Status (e.g., "NZ need 239 runs")
        status_tag = link_tag.find("span", class_="text-cbLive") or link_tag.find("span", class_="text-cbPreview")
        status = status_tag.text.strip() if status_tag else "N/A"

        match_data.append({
            "match": title,
            "scores": scores,
            "status": status
        })
    
    return match_data