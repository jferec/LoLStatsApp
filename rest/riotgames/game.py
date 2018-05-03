import requests
import json, time
import rest.riotgames.key
from rest.models import Game
from rest.riotgames.key import Key


def create_game(region, match_id):
    api_key = Key().api_key
    url = 'https://' + str(region) + '.api.riotgames.com/lol/match/v3/timelines/by-match/' + str(match_id)
    header = {"X-Riot-Token": api_key}
    response = requests.get(url, headers=header).text
    json_obj = json.loads(response)
    #_  _game lists gather all _player lists
    creep_score_game, experience_game, level_game, gold_game = ([] for i in range(4))
    #   _player lists gather individual data
    creep_score_player, experience_player, level_player, gold_player = ([] for i in range(4))

    frames = json_obj['frames']
    #   Collects data iterating through 'frames' each belonging to a single player
    #   Gathered _player data is stored in a list and then added to _game list
    #   Blue team players : [1, 2, 3, 4, 5...    Read team players : ...6, 7, 8, 9, 10] ('participantId')
    for y in range(1, 11):
        for x in range(len(frames)):
            creep_score_player.append(frames[x]['participantFrames'][str(y)]['minionsKilled'] + frames[x]['participantFrames']['1']['jungleMinionsKilled'])
            experience_player.append(frames[x]['participantFrames'][str(y)]['xp'])
            level_player.append(frames[x]['participantFrames'][str(y)]['level'])
            gold_player.append(frames[x]['participantFrames'][str(y)]['totalGold'])
    #   Adding _player's lists to _game's lists
        creep_score_game.append(creep_score_player)
        experience_game.append(experience_player)
        level_game.append(level_player)
        gold_game.append(gold_player)
    #   Clearing individual player lists
        creep_score_player, experience_player, level_player, gold_player = ([] for i in range(4))

    url = 'https://' + region + '.api.riotgames.com/lol/match/v3/matches/' + match_id + '?api_key='
    response = requests.get(url + api_key).text
    json_obj = json.loads(response)

    #   Basic game info
    game_id = json_obj["gameId"]
    game_duration = json_obj["gameDuration"]
    game_date = int(json_obj['gameCreation'])/1000
    blue_team_win = False if json_obj['teams'][0]['win'] == 'Fail' else True

    dmg_to_champions_game, dmg_taken_game, kda_game, champions_game, item_set_game, lane_game, vision_score_game = ([] for i in range(7))
    dmg_to_champions_player, dmg_taken_player, kda_player, item_set_player = ([] for i in range(4))
#   final_ is a prefix for stats that already where tracked in a time line
    final_creep_score_game, final_gold_game, final_level_game = ([] for i in range(3))

    frames = json_obj['participants']

    for y in range(0, 10):
        dmg_to_champions_player.append(frames[y]['stats']['physicalDamageDealtToChampions'])
        dmg_to_champions_player.append(frames[y]['stats']['magicDamageDealtToChampions'])
        dmg_to_champions_player.append(frames[y]['stats']['trueDamageDealtToChampions'])
        dmg_taken_player.append(frames[y]['stats']['physicalDamageTaken'])
        dmg_taken_player.append(frames[y]['stats']['magicalDamageTaken'])
        dmg_taken_player.append(frames[y]['stats']['trueDamageTaken'])
        kda_player.append(frames[y]['stats']['kills'])
        kda_player.append(frames[y]['stats']['deaths'])
        kda_player.append(frames[y]['stats']['assists'])
        final_gold_game.append(frames[y]['stats']['goldEarned'])
        final_level_game.append(frames[y]['stats']['champLevel'])
        lane_game.append(frames[y]['timeline']['lane'])
        final_creep_score_game.append(frames[y]['stats']['totalMinionsKilled'] + frames[y]['stats']['neutralMinionsKilled'])
        vision_score_game.append(frames[y]['stats']['visionScore'])
        champions_game.append(frames[y]['championId'])
        for x in range(0, 7):
            item_set_player.append(frames[y]['stats']['item'+str(x)])
        dmg_to_champions_game.append(dmg_to_champions_player)
        dmg_taken_game.append(dmg_taken_player)
        kda_game.append(kda_player)
        item_set_game.append(item_set_player)
    #   Clearing _player lists
        dmg_to_champions_player, dmg_taken_player, kda_player, item_set_player = ([] for i in range(4))

    q = Game()
    q.region = region
    q.id = game_id
    q.game_duration = game_duration
    q.game_date = game_date
    q.blue_team_win = blue_team_win
    q.champion = champions_game
    q.lane = lane_game
    q.final_item_set = item_set_game
    q.final_creep_score = final_creep_score_game
    q.ts_creep_score = creep_score_game
    q.ts_experience = experience_game
    q.final_level = final_level_game
    q.ts_level = level_game
    q.final_gold = final_gold_game
    q.ts_gold = gold_game
    q.final_dmg_to_champions = dmg_to_champions_game
    q.final_dmg_taken = dmg_taken_game
    q.final_kda = kda_game
    q.final_vision_score = vision_score_game
    q.created = int(time.time())
    q.save()
    return q
