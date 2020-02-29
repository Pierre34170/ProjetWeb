from django.urls import path
from . import views
from proposition import views as proposition_views
from proposition.views import (
	PropositionListView, 
	PropositionDetailView, 
	PropositionCreateView,
	PropositionUpdateView,
	PropositionDeleteView,
    TrainingListView,
    TrainingDetailView,
    TrainingCreateView,
    TrainingUpdateView,
    TrainingDeleteView,
    TeamCreateView,
    FindMatch
)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
#    path('organize/', proposition_views.organize_view, name='organize'),
    path('proposition_list/', FindMatch, name='proposition_list'),
    path('proposition/<int:pk>', PropositionDetailView.as_view(), name='proposition_detail'),
    path('proposition/new/', PropositionCreateView.as_view(), name='proposition_create'),
    path('proposition/<int:pk>/update/', PropositionUpdateView.as_view(), name='proposition_update'),
    path('proposition/<int:pk>/delete/', PropositionDeleteView.as_view(), name='proposition_delete'),
    path('training_list/', TrainingListView.as_view(), name='training_list'),
    path('training/<int:pk>/', TrainingDetailView.as_view(), name='training_detail'),
    path('training/new/', TrainingCreateView.as_view(), name='training_create'), 
    path('training/<int:pk>/update/', TrainingUpdateView.as_view(), name='training_update'),
    path('training/<int:pk>/delete/', TrainingDeleteView.as_view(), name='training_delete'),
    path('team/new/', TeamCreateView.as_view(), name='team_create')
]
