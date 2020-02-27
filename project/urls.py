from django.urls import path
from . import views
from proposition import views as proposition_views
from proposition.views import (
	PropositionListView, 
	PropositionDetailView, 
	PropositionCreateView,
	PropositionUpdateView,
	PropositionDeleteView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('organize/', proposition_views.organize_view, name='organize'),
    path('proposition_list/', PropositionListView.as_view(), name='proposition_list'),
    path('proposition/<int:pk>', PropositionDetailView.as_view(), name='proposition_detail'),
    path('proposition/new/', PropositionCreateView.as_view(), name='proposition_create'),
    path('proposition/<int:pk>/update/', PropositionUpdateView.as_view(), name='proposition_update'),
    path('proposition/<int:pk>/delete/', PropositionDeleteView.as_view(), name='proposition_delete'),

]
