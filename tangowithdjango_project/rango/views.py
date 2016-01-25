from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict ={}
    return render(request, 'rango/about.html', context_dict)
