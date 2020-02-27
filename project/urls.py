from django.urls import path
from . import views
from proposition import views as proposition_views
from proposition.views import PropositionListView, PropositionDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('organize/', proposition_views.organize_view, name='organize'),
    path('proposition_list/', PropositionListView.as_view(), name='proposition_list'),
    path('proposition_list/proposition/<int:pk>', PropositionDetailView.as_view(), name='proposition_detail'),
]


#display_game.html