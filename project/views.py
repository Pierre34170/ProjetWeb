from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return render(request, 'project/home.html')

def about(request):
	return render(request, 'project/about.html', {'title': 'About'})
