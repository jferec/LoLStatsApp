import requests
import json, time
from rest.riotgames.key import Key

from rest.models import Player


def create_player(region, summoner_name):

    api_key = Key().api_key
    url = 'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + str(summoner_name)
    header = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=header).text
    json_obj = json.loads(response)
    q = Player()
    q.id = json_obj['id']
    q.account_id = json_obj['accountId']
    q.summoner_name = json_obj['name']
    q.profile_icon_id = json_obj['profileIconId']
    q.summoner_level = json_obj['summonerLevel']
    q.region = region

    url = 'https://' + region + '.api.riotgames.com/lol/league/v3/positions/by-summoner/' + q.id
    response = requests.get(url, header=header).text
    json_obj = json.loads(response)
    for x in range(len(json_obj)):
        if json_obj[x]['queueType'] == 'RANKED_SOLO_5x5':
            q.ranked_wins = json_obj[x]['wins']
            q.ranked_losses = json_obj[x]['losses']
            q.ranked_tier = json_obj[x]['tier'].title()
            q.ranked_division = json_obj[x]['rank']
            q.league_points = json_obj[x]['leaguePoints']
            break

    if q.ranked_division is None:
        q.ranked_wins = 0
        q.ranked_losses = 0
        q.ranked_tier = 'Unranked'
        q.ranked_tier = None
        q.league_points = 0

    q.last_update = int(json_obj['revisionDate']/1000)
    q.save()


def update_player(player):
    api_key = Key().api_key

