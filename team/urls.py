from django.urls import path, include
from .views import *


urlpatterns = [
	path('team/new/', TeamCreateView.as_view(), name='team_create'),
    path('', MyTeams, name='team_list' ),
    path('team/detail/<int:pk>/', MyTeamDetail, name='team_detail'),
    path('team/player/<int:pk>/delete/', DeleteMyPlayers, name='delete_player' ),
    path('team/<int:pk>/delete/', DeleteMyTeam, name='delete_team'),
    path('research_team/', ResearchTeam, name='research_team'),
    path('team/<int:pk>/',JoinTeam , name='join_team'),
]