import requests
import re
import json
import pandas as pd
from pathlib import Path

# local server neeeds to be running:
# API lokal starten:
# git clone https://github.com/DanielWTE/ebay-kleinanzeigen-api.git
# cd ebay-kleinanzeigen-api
# pip install -r requirements.txt
# playwright install chromium
# uvicorn main:app --reload

BASE_URL = "http://localhost:8000"


def extract_id_from_url(url):
    match = re.search(r'/(\d+)-', url)
    return match.group(1) if match else None

def save_json(data, filename="results.json"):
    """Save Python object to a JSON file with pretty formatting."""
    path = Path(filename)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved JSON to {path.resolve()}")

def save_json_as_excel(data, filename="results.xlsx"):
    df = pd.json_normalize(data)
    df.to_excel("results.xlsx", index=False)
    
def search_offers(query: str, location: str = None, radius: int = None,
                  min_price: int = None, max_price: int = None, page_count: int = 1):
    params = {"query": query}
    if location:
        params["location"] = location
    if radius:
        params["radius"] = radius
    if min_price:
        params["min_price"] = min_price
    if max_price:
        params["max_price"] = max_price
    if page_count:
        params["page_count"] = page_count

    response = requests.get(f"{BASE_URL}/inserate", params=params)
    response.raise_for_status()
    return response.json()

def get_offer_detail(offer_id: str):
    response = requests.get(f"{BASE_URL}/inserat/{offer_id}")
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Step 1: Search for offers (preview data)
    search_results = search_offers("Reihenhaus", location="90763", radius=5,
                                   min_price=100000, max_price=800000, page_count=5)

    num_found = len(search_results.get("data", []))
    if num_found == 0:
        print("No offers found.")
    else:
        print(f"Found {num_found} offers matching the search criteria.")

    # Step 2: Fetch full details for each offer
    full_results = []
    details_cnt = 0
    for offer in search_results.get("data", []):
        details_cnt += 1
        print(f"Fetching details for offer {details_cnt}/{num_found}...")
        offer_id = extract_id_from_url(offer.get("url", ""))
        if offer_id:
            try:
                details = get_offer_detail(offer_id)
                categories_list = details["data"]["categories"]
                if "Häuser zum Kauf" in categories_list:
                    # Merge preview data and full details
                    merged = {**offer, **details["data"]}
                    full_results.append(merged)
                #if details_cnt > 2:
                #    break
            except requests.HTTPError as e:
                print(f"Error fetching details for ID {offer_id}: {e}")

    # Step 3: Save full data with full descriptions
    save_json(full_results, "results_full.json")
    save_json_as_excel(full_results, "results_full.xlsx")

