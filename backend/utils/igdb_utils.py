import os

client_id = os.getenv("IGDB_CLIENT_ID")

def get_client_secret():
    return os.getenv("IGDB_CLIENT_SECRET")