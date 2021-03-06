from rest_framework import serializers
from rest.models import Game, Player


class GameGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'region', 'game_duration', 'game_date', 'lane', 'final_level', 'champion',
                  'blue_team_win', 'final_item_set', 'final_creep_score',
                  'ts_creep_score', 'ts_experience', 'final_level',
                  'ts_level', 'final_gold', 'ts_gold', 'final_dmg_to_champions',
                  'final_dmg_taken', 'final_kda', 'final_vision_score', 'created',)


class GameFromIdAndRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'region',)


class PlayerFromNameAndRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('summoner_name', 'region',)


class PlayerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'account_id', 'region', 'summoner_name',
                  'profile_icon_id', 'summoner_level', 'ranked_tier',
                  'ranked_division', 'ranked_wins', 'ranked_losses', 'last_update',)