from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html', {})


def category(request, category_name_slug):
    context_dict = {}

    try:
        # Try search for the slug in the model. If we can't find it the methods raise an DoesNotExist exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)  # Retrieve all the associated pages.
        context_dict['pages'] = pages  # Add result to the dictionary.
        context_dict['category'] = category  # Also add the category object to the dictionary.
        context_dict['category_name_slug'] = category_name_slug

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)  # Save form if we are provided with valid data

            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)  # Hash the password
            user.save()  # Save the password

            profile = profile_form.save(commit=False)
            profile.user = user

            #  Check if user provides a profile picture
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    # If this is not a HTTP POST, then render the forms for input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):

    # If request is POST, pull out relevant information
    if request.method == 'POST':
        # Gather the username and password provided the user from the login form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use django's own authenticate method to see if the username and password combination is correct.
        user = authenticate(username=username, password=password)

        # If the user state exists
        if user:

            # Check if the user account is active (could be disabled).
            if user.is_active:
                # If the user is valid and active, log the user in.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # If an inactive account was used.
                return HttpResponse('Your Rango account is disabled.')

        else:
            # Bad login details were provided. Unsuccessful login.
            print 'Invalid login details: {0}, {1}'.format(username, password)
            return HttpResponse('Invalid login details supplied.')

    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
    logout(request)  # Since we now the user is logged in, we can just log em out.
    return HttpResponseRedirect('/rango/')  # Redirect back to home page.

