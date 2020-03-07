from django.urls import path
from .views import *


urlpatterns = [
	path('', MyTrainings, name='training_list'),
	path('new/', SuggestTraining, name='training_create'), 
    path('training/<int:pk>/', TrainingDetailView.as_view(), name='training_detail'),
    path('training/<int:pk>/update/', TrainingUpdateView.as_view(), name='training_update'),
    path('training/<int:pk>/delete/', TrainingDeleteView.as_view(), name='training_delete'),
]