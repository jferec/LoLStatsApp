import requests
import json, time
from rest.riotgames.key import Key

from rest.models import Player


def create_player(region, summoner_name):
    api_key = Key().api_key
    json_obj = json.loads(riot_api_summoner_by_name(region, summoner_name, api_key))
    q = Player()
    q.id = json_obj['id']
    q.account_id = json_obj['accountId']
    q.summoner_name = json_obj['name']
    q.profile_icon_id = json_obj['profileIconId']
    q.summoner_level = json_obj['summonerLevel']
    q.region = region
    q.last_update = int(json_obj['revisionDate'] / 1000)
    json_obj = json.loads(riot_api_league_by_summoner(region, q.id, api_key))
    assign_player_stats(q, json_obj)
    return q


def update_player(player):
    api_key = Key().api_key
    json_obj = json.loads(riot_api_summoner_by_name(player.region, player.summoner_name, api_key))
    player.summoner_name = json_obj['name']
    player.profile_icon_id = json_obj['profileIconId']
    player.summoner_level = json_obj['summonerLevel']
    player.last_update = int(json_obj['revisionDate']/1000)
    json_obj = json.loads(riot_api_league_by_summoner(player.region, player.id, api_key))
    assign_player_stats(player, json_obj)
    return player


def riot_api_summoner_by_name(region, summoner_name, api_key):
    url = 'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + str(summoner_name)
    header = {"X-Riot-Token": api_key}
    return requests.get(url, headers=header).text


def riot_api_league_by_summoner(region, id, api_key):
    url = 'https://' + region + '.api.riotgames.com/lol/league/v3/positions/by-summoner/' + str(id)
    header = {"X-Riot-Token": api_key}
    return requests.get(url, headers=header).text


def assign_player_stats(player, json_obj):
    for x in range(len(json_obj)):
        if json_obj[x]['queueType'] == 'RANKED_SOLO_5x5':
            player.ranked_wins = json_obj[x]['wins']
            player.ranked_losses = json_obj[x]['losses']
            player.ranked_tier = json_obj[x]['tier'].title()
            player.ranked_division = json_obj[x]['rank']
            player.league_points = json_obj[x]['leaguePoints']
            break

    if player.ranked_division is None:
        player.ranked_wins = 0
        player.ranked_losses = 0
        player.ranked_tier = 'Unranked'
        player.ranked_tier = None
        player.league_points = 0

    player.save()





