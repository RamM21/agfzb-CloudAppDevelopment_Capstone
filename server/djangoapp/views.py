from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context={}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html',context)



# Create a `contact` view to return a static contact page
def contact(request):
    context={}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html',context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/ff38d0f2-e12e-497f-a5ea-d8452b7b4737/default/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request,dealer_id):
    if request.method == "GET":
        context = {}
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/ff38d0f2-e12e-497f-a5ea-d8452b7b4737/default/get-review"
        reviews = get_dealer_reviews_from_cf(url, id=dealer_id)
        context["review"] = reviews
        context["dealer"] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        if request.method=='GET':
            context={}
            cars = CarModel.objects.all()
            context["cars"] = cars
            context["dealer"]=dealer_id
            return render(request, 'djangoapp/add_review.html', context)
        if request.method=='POST':
            url = "https://eu-de.functions.appdomain.cloud/api/v1/web/ff38d0f2-e12e-497f-a5ea-d8452b7b4737/default/post-review"
            rev={}
            json_payload={}
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            rev["name"] = request.user.username
            rev["review"] = request.POST["content"]
            rev["dealership"] = dealer_id
            rev["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    rev["purchase"] = True
            rev["time"] = datetime.utcnow().isoformat()
            rev["purchase_date"] = request.POST["purchase_date"]
            rev["car_make"] = car.car.name
            rev["car_model"] = car.name
            rev["car_year"] = int(car.year.strftime("%Y"))
            json_payload["review"] = rev
            result = post_request(url,json_payload,id=dealer_id)
            print(result)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


