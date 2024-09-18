import os
import requests
from dotenv import load_dotenv


def get_first_price(game_id:str, since:str):
    load_dotenv()
    params = {
        'key': os.getenv("ITAD_API_KEY"),
        'id': game_id,
        'since': since
    }
    resp = requests.get("https://api.isthereanydeal.com/games/history/v2", params=params)
    resp.raise_for_status()
    if resp.status_code == 200:
        if len(resp.json()) > 1:
            return resp.json()[-1]

def get_game(game_name:str):
    load_dotenv()
    params = {
        'key': os.getenv("ITAD_API_KEY"),
        'title': f'{game_name}',
    }
    resp = requests.get("https://api.isthereanydeal.com/games/lookup/v1", params=params)
    resp.raise_for_status()
    return resp.json()

#get_game("ssx")
get_first_price("018d937f-1b4a-717f-8ff4-08a19cab628e","2000-06-27T00:00:00+00:00")
