from django.urls import path
from . import views
from proposition import views as proposition_views
from proposition.views import (
	PropositionListView, 
#	PropositionDetailView, 
	PropositionCreateView,
	PropositionUpdateView,
	PropositionDeleteView,
    TrainingListView,
    TrainingDetailView,
    TrainingCreateView,
    TrainingUpdateView,
    TrainingDeleteView,
    TeamCreateView,
    TeamDeleteView,
    TeamListView,
    MyTeams,
#    MatchCreateView,
    ResearchMatch,
    SuggestTraining,
    Reservation,
    DetailProposition,
    MyResponse,
    MyTrainings,
    MyMatchs,
    DetailMatch,
    involveTeam,

)
from account.views import (
    MyTeamDetail,
    DeleteMyPlayers,
    DeleteMyTeam
    )

urlpatterns = [
    path('', views.home, name='home'),
#    path('about/', views.about, name='about'),
#    path('organize/', proposition_views.organize_view, name='organize'),
    path('proposition_list/', ResearchMatch, name='proposition_list'),
    path('proposition/<int:pk>', DetailProposition, name='proposition_detail'),
    path('proposition/new/', PropositionCreateView.as_view(), name='proposition_create'),
    path('proposition/<int:pk>/update/', PropositionUpdateView.as_view(), name='proposition_update'),
    path('proposition/<int:pk>/delete/', PropositionDeleteView.as_view(), name='proposition_delete'),

    path('proposition/<int:pk>/confirm', Reservation, name='confirmation' ),
    path('proposition/<int:pk>/confirm/chooseyourteam/', involveTeam, name='choose'),

    path('responses/', MyResponse, name='proposition_response'),

    path('matchs/', MyMatchs, name='matchs'),
    path('matchs/<int:pk>/', DetailMatch, name='matchs_detail'),

    path('training_list/', MyTrainings, name='training_list'),
    path('training/<int:pk>/', TrainingDetailView.as_view(), name='training_detail'),
    path('training/new/', SuggestTraining, name='training_create'), 
    path('training/<int:pk>/update/', TrainingUpdateView.as_view(), name='training_update'),
    path('training/<int:pk>/delete/', TrainingDeleteView.as_view(), name='training_delete'),


    path('team/new/', TeamCreateView.as_view(), name='team_create'),
    path('team_list/', MyTeams, name='team_list' ),
    path('team/detail/<int:pk>/', MyTeamDetail, name='team_detail'),
    path('team/player/<int:pk>/delete/', DeleteMyPlayers, name='delete_player' ),
    path('team/<int:pk>/delete/', DeleteMyTeam, name='delete_team'),
#    path('match/new/', MatchCreateView.as_view(), name='match_create')
]
