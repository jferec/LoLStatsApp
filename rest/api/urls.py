from.views import GamePostRudView, PlayerPostRudView, GamePostAPIView, PlayerPostAPIView
from django.urls import path

app_name = "rest"

urlpatterns = [
    path('game/<int:id>/', GamePostRudView.as_view(), name='post-rud'),
    path('player/<int:id>/', PlayerPostRudView.as_view(), name='post-rud-1'),
    path('game/', GamePostAPIView.as_view(), name='post-create'),
    path('player/', PlayerPostAPIView.as_view(), name='post-create-1'),
]
