from django.urls import path
from .views import *


urlpatterns = [
    path('', ResearchMatch, name='proposition_list'),
    path('new/', PropositionCreateView.as_view(), name='proposition_create'),
    path('proposition/<int:pk>/', DetailProposition, name='proposition_detail'),
    path('proposition/<int:pk>/update/', PropositionUpdateView.as_view(), name='proposition_update'),
    path('proposition/<int:pk>/delete/', PropositionDeleteView.as_view(), name='proposition_delete'),
    path('proposition/<int:pk>/confirm/', Reservation, name='confirmation' ),
    path('responses/', MyResponse, name='proposition_response'),
    path('responses/match/<int:pk>/', DetailMatch, name='matchs_detail'),
    path('matchs/', MyMatchs, name='matchs'),
]