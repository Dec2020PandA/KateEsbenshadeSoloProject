from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def login(request):
    return render(request, 'login.html')

def sign_up(request):
    return render(request, 'sign_up.html')

def create_user(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user_pw=request.POST['password']
            hash_pw=bcrypt.hashpw(user_pw.encode(),bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                description = request.POST['description'],
                location = request.POST['location'],
                password = hash_pw,
            )
            request.session['user_id']=new_user.id
            request.session['user_firstname']=new_user.first_name
            request.session['user_lastname']=new_user.last_name
            request.session['user_email']=new_user.email
            request.session['user_description']=new_user.description
            request.session['user_location']=new_user.location
            return redirect('/home')
    else:
        return redirect('/')

def log_user(request):
    if request.method == "POST":
        logged_user = User.objects.filter(email=request.POST['login_email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_firstname']=logged_user.first_name
                request.session['user_lastname']=logged_user.last_name
                request.session['user_email']=logged_user.email
                request.session['user_description']=logged_user.description
                request.session['user_location']=logged_user.location
                return redirect('/home')
    return redirect('/')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['user_id']),
        'actions' : Action.objects.all
    }
    return render(request, "home.html", context)


def why(request):
    return render(request, "why.html")


def totals(request):
    count = Action.objects.all().count()
    context = {
        'count' : Action.objects.all().count(),
        'transport_count' : Action.objects.filter(topic = "Transportation").count(),
        'waste_count' : Action.objects.filter(topic = "Waste").count(),
        'food_count' : Action.objects.filter(topic = "Diet").count(),
        'nature_count' : Action.objects.filter(topic = "Nature").count(),
        'home_count' : Action.objects.filter(topic = "Improvements").count(),
    }
    return render(request, "totals.html", context)

def add_action_page(request):
    return render(request, "add_action_page.html")

def process_action(request):
    if request.method=="POST":
        Action.objects.create(
            title = request.POST['title'],
            topic = request.POST['topic'],
            description = request.POST['description'],
            creator = User.objects.get(id=request.session['user_id']),
        )
        return redirect('/add')
    return redirect('/add')

def profile(request, id):
    context = {
        'user' : User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def topic_prof(request, topic):
    context = {
        'topic': Action.objects.filter(topic=topic)
    }
    return render(request, 'topic_prof.html', context)

def action_prof(request, action_id):
    context = {
        'action': Action.objects.get(id=action_id)
    }
    return render(request, 'action_prof.html', context)

def add_to_do(request, id):
    user = User.objects.get(id=request.session["user_id"])
    action = Action.objects.get(id=id)
    user.actions_to_do.add(action)
    return redirect('/home')

def remove_to_do(request, id):
    user = User.objects.get(id=request.session["user_id"])
    action = Action.objects.get(id=id)
    user.actions_to_do.remove(action)
    return redirect('/home')

def delete(request, id):
    action = Action.objects.get(id=id)
    action.delete()
    return redirect('/home')

def to_do(request):
    context = {
        "user" : User.objects.get(id=request.session["user_id"])
    }
    return render(request, "to_do.html", context)