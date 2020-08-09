
"""Devotion: fetches daily devotion"""

from secret import API_KEY
import requests

class Devotion():

    def __init__(self):

    def get_daily_devotion():
        """Make API requests to return daily devotion"""
        resp = requests.get(https://devotionalium.com/api/v2?lang=en)

        return resp.json()

        

        # resp = requests.get(f"https://newsapi.org/v2/top-headlines", {"category": "sports", "pageSize": 7, "country": lang, "apiKey": API_KEY})