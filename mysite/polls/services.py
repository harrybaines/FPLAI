import requests


def get_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    r = requests.get(url, params={})
    json = r.json()
    return json


def get_managers_team(manager_id):
    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/"
    r = requests.get(url, params={})
    json = r.json()
    return json