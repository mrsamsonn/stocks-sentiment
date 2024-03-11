from django.shortcuts import render
from .script import func

def index(request):
    output = func
    return render(request, 'index.html', {'output': output})
