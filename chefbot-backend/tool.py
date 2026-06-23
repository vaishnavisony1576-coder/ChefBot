import requests
import random
import os
from dotenv import load_dotenv
load_dotenv()
def fetch_image(dish_name):
    import requests

    API_KEY = os.getenv("PEXELS_API_KEY")

    try:
        url = "https://api.pexels.com/v1/search"
        headers = {
            "Authorization": API_KEY
        }

        params = {
            "query": dish_name + " food",
            "per_page": 1
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        if data["photos"]:
            return data["photos"][0]["src"]["medium"]
        else:
            return "https://via.placeholder.com/300"

    except Exception as e:
        print("PEXELS ERROR:", e)
        return "https://via.placeholder.com/300"