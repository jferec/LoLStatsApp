from rest.api.views import CreateOrGetGame, CreateOrUpdatePlayer
from django.urls import path

app_name = "rest"

urlpatterns = [
    path('game/', CreateOrGetGame.as_view(), name='post-create'),
    path('player/', CreateOrUpdatePlayer.as_view(), name='post-create-1'),
]
