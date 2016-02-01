from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page


def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)


def about(request):
    context_dict ={}
    return render(request, 'rango/about.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}

    try:
        # Try search for the slug in the model. If we can't find it the methods raise an DoesNotExist exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)  # Retrieve all the associated pages.
        context_dict['pages'] = pages  # Add result to the dictionary.
        context_dict['category'] = category  # Also add the category object to the dictionary.

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

