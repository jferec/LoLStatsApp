#generic
from django.http import HttpResponse
from rest_framework import status, response
from rest.models import Game, Player
from rest_framework import generics, mixins
from.serializers import PlayerFromNameAndRegionSerializer, GameFromIdAndRegionSerializer, GameGetSerializer, PlayerPostSerializer
from rest.riotgames.game import create_game
from rest.riotgames.player import create_player, update_player
from django.core import serializers
from rest_framework.decorators import api_view


class CreateOrGetGame(generics.ListAPIView):
    serializer_class = GameGetSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        region = self.request.query_params.get('region', None)
        queryset = Game.objects.filter(id=id, region=region)
        if not queryset:
            create_game(region, id)
            queryset = Game.objects.filter(id=id, region=region)
        return queryset


class CreateOrUpdatePlayer(generics.CreateAPIView):
    serializer_class = PlayerFromNameAndRegionSerializer
##FIX DOUBLE REQUESTS!!!!!!!

    def post(self, request, *args, **kwargs):
        serializer = PlayerFromNameAndRegionSerializer(data=request.data)
        if serializer.is_valid():
            region = request.POST.get("region")
            summoner_name = request.POST.get("summoner_name")
            queryset = Player.objects.filter(summoner_name=summoner_name, region=region)
            if queryset:
                update_player(queryset)
                queryset = Player.objects.filter(summoner_name=summoner_name, region=region)
            else:
                create_player(region, summoner_name)
                queryset = Player.objects.filter(summoner_name=summoner_name, region=region)

            return HttpResponse(status.HTTP_201_CREATED)
        return HttpResponse(status.HTTP_404_NOT_FOUND)




