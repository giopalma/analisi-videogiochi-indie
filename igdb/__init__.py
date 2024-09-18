import ast
import requests
import time
import pandas as pd


class IGDBWrapper:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }

        resp = requests.post(
            "https://id.twitch.tv/oauth2/token", params=params)
        resp.raise_for_status()

        data = resp.json()
        self.bearer_token = data['access_token']

    def games(self, body: str):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer {}'.format(self.bearer_token)
        }
        resp = requests.post("https://api.igdb.com/v4/games",
                             headers=headers, data=body)
        resp.raise_for_status()
        return resp.json()

    def genres(self):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer {}'.format(self.bearer_token)
        }
        query = 'fields name; limit 100;'
        resp = requests.post("https://api.igdb.com/v4/genres",
                             headers=headers, data=query)
        resp.raise_for_status()
        return resp.json()

    def game_engines(self, query):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer {}'.format(self.bearer_token)
        }
        resp = requests.post("https://api.igdb.com/v4/game_engines",
                             headers=headers, data=query)
        resp.raise_for_status()
        return resp.json()

    def fetch_all_games(self):
        print("Inizio del fetch...")
        all_games = []
        limit = 500  # IGDB consente fino a 500 risultati per richiesta
        offset = 0  # Inizia dall'inizio

        while True:
            query = f"""
            fields id, name, genres, aggregated_rating, aggregated_rating_count;
            where aggregated_rating != null & genres != null;
            limit {limit};
            offset {offset};
            """

            games = self.games(query)
            if not games:  # Se non ci sono più risultati, esci dal ciclo
                break

            all_games.extend(games)
            offset += limit  # Incrementa l'offset per la prossima richiesta
            time.sleep(0.25)
        data = pd.DataFrame(all_games)
        data.to_csv("data/igdb.csv", index=False)
        print("Fine del fetch...")
        return all_games

    def fetch_all_game_engines(self):
        print("Inizio del fetch...")
        all_game_engines = []
        limit = 500  # IGDB consente fino a 500 risultati per richiesta
        offset = 0  # Inizia dall'inizio

        while True:
            query = f"""
            fields *;
            limit {limit};
            offset {offset};
            """

            game_engines = self.game_engines(query)
            if not game_engines:  # Se non ci sono più risultati, esci dal ciclo
                break

            all_game_engines.extend(game_engines)
            offset += limit  # Incrementa l'offset per la prossima richiesta
            time.sleep(0.25)
        data = pd.DataFrame(all_game_engines)
        data.to_csv("data/igdb_game_engines.csv", index=False)
        print("Fine del fetch...")
        return all_game_engines

    def websites(self, query):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer {}'.format(self.bearer_token)
        }
        resp = requests.post("https://api.igdb.com/v4/websites",
                             headers=headers, data=query)
        resp.raise_for_status()
        return resp.json()

    def fetch_all_websites(self):
        print("Inizio del fetch...")
        all_websites = []
        limit = 500  # IGDB consente fino a 500 risultati per richiesta
        offset = 0  # Inizia dall'inizio

        while True:
            query = f"""
            fields *;
            limit {limit};
            offset {offset};
            """
            websites = self.websites(query)
            if not websites:  # Se non ci sono più risultati, esci dal ciclo
                break

            all_websites.extend(websites)
            offset += limit  # Incrementa l'offset per la prossima richiesta
            time.sleep(0.25)
        data = pd.DataFrame(all_websites)
        data.to_csv("data/igdb_websites.csv", index=False)
        print("Fine del fetch...")
        return all_websites
