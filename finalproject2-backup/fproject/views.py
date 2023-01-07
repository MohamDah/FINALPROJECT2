from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, resolve
from django.contrib.auth.decorators import login_required
#from django.views.decorators.csrf import csrf_exempt

#from django.core.paginator import Paginator

import datetime
import json
from django.core import serializers

from .models import User, friend_request, message

# Create your views here.

@login_required(login_url='/login')
def index(request):
    return render(request, "fproject/index.html") 


def login_view(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "fproject/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "fproject/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "fproject/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "fproject/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "fproject/register.html")

@login_required(login_url='/login')
def explore(request):
    users = User.objects.all()
    requestfrom = friend_request.objects.filter(requested=request.user).values_list('requestor', flat=True)
    requestto = friend_request.objects.filter(requestor=request.user).values_list('requested', flat=True)
    friends = request.user.friends.all()
    return render(request, "fproject/explore.html", {
        "users": users,
        "requestfrom": requestfrom,
        "requestto": requestto,
        "friends": friends
    })

@login_required(login_url='/login')
def send_request(request):
    if request.method == "POST":
        requestor = request.user
        requested = User.objects.get(id=request.POST["target"])
        if friend_request(requestor=requestor, requested=requested).is_valid_request() == False:
            return HttpResponse("<h1 style='color:red; margin:50px;'>Can't send request to self</h1>")

        if request.POST["reason"] == "send":
            frequest, created = friend_request.objects.get_or_create(requestor=requestor, requested=requested)
            if created:
                return HttpResponseRedirect(reverse("explore"))
            else:
                return HttpResponse("<h1 style='color:red'>Already sent</h1>")
        
        elif request.POST["reason"] == "remove":
            r = friend_request.objects.get(requestor=requestor, requested=requested)
            r.delete()
            return HttpResponseRedirect(reverse("explore"))


def notifications(request):
    if request.method == "POST":
        pass
    else:
        reqs = friend_request.objects.filter(requested=request.user)
        return render(request, "fproject/notifications.html", {
            "reqs": reqs
        })

@login_required(login_url='/login')
def friends(request):
    if request.method == "POST":
        requestor = request.user
        requested = User.objects.get(id=request.POST["target"])
        if friend_request(requestor=requestor, requested=requested).is_valid_request() == False:
            return HttpResponse("<h1 style='color:red; margin:50px;'>Can't send request to self</h1>")

        if request.POST["reason"] == "accept":
            try:
                    friend_request.objects.get(requestor=requested, requested=requestor)
            except:
                return HttpResponse("<h1 style='color:red; margin:50px;'>don't try to forge requests</h1>")
            requestor.friends.add(requested)
            requested.friends.add(requestor)
            r = friend_request.objects.get(requestor=requested, requested=requestor)
            r.delete()
            
        elif request.POST["reason"] == "unfriend":
            if requested not in requestor.friends.all():
                return render(request, "fpoject/apology.html", {
                    "message": "don't try to forge requests"
                })
            
            requestor.friends.remove(requested)
            requested.friends.remove(requestor)

        return HttpResponseRedirect(reverse("friends"))
    else:
        friends = request.user.friends.all()
        return render(request, "fproject/friends.html", {
            "friends": friends
        })


@login_required(login_url='/login')
def chat(request, username):
    u1 = request.user
    u2 = User.objects.get(username=username)
    if u2 not in u1.friends.all():
        return render(request, "fpoject/apology.html", {
            "message": "You're not friends with this user"
        })

    try:
        u1_messages = message.objects.filter(message_sender=u1, message_reciever=u2)
    except:
        u1_messages = []
    
    try:
        u2_messages = message.objects.filter(message_sender=u2, message_reciever=u1)
    except:
        u2_messages = []
    
    messages = u1_messages | u2_messages
    
    messages = messages.order_by("date")

    return render(request, "fproject/chat.html", {
        "messages": messages,
        "u2": u2
    })

def send_message(request):
    if request.method == "POST":
        u1 = request.user
        u2 = User.objects.get(id=request.POST["target"])
        date = datetime.datetime.now()
        text = request.POST["text"]
        mess = message(message_sender=u1, message_reciever=u2, message=text, date=date)
        mess.save()
        return HttpResponseRedirect(reverse("chat", args=(u2.username,)))

def json_chat(request, username):
    u1 = request.user
    u2 = User.objects.get(username=username)
    if u2 not in u1.friends.all():
        return render(request, "fpoject/apology.html", {
            "message": "You're not friends with this user"
        })

    try:
        u1_messages = message.objects.filter(message_sender=u1, message_reciever=u2)
    except:
        u1_messages = []
    
    try:
        u2_messages = message.objects.filter(message_sender=u2, message_reciever=u1)
    except:
        u2_messages = []
    
    messages = u1_messages | u2_messages
    
    messages = messages.order_by("date")

    return JsonResponse([m.serialize() for m in messages], safe=False)