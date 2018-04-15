#generic
from rest.models import Game, Player
from rest_framework import generics, mixins
from.serializers import GamePostSerializer, PlayerPostSerializer
from rest.riotgames.game import create_game
from rest.riotgames.player import create_player


class GamePostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Game.objects.all()
    serializer_class = GamePostSerializer

    def get_queryset(self):
        return Game.objects.all()


class PlayerPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Player.objects.all()
    serializer_class = PlayerPostSerializer

    def get_queryset(self):
        return Player.objects.all()


class GamePostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'id'
    queryset = Game.objects.all()
    serializer_class = GamePostSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            create_game(query)


class PlayerPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_fields = 'id', 'euw'
    queryset = Player.objects.all()
    serializer_class = PlayerPostSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            create_player(query)


