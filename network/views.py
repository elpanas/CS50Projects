import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime  
from .models import User, Message, Follow, Likes
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def index(request):    
    if (request.method == "POST"):        
        mes = Message(body = request.POST["textpost"],
                      user = request.user)
        mes.save()

    posts = Message.objects.all().order_by('-date')

    p = Paginator(posts, 10) # organize posts in pages

    if request.GET.get('page') is not None:
        page_number = request.GET.get('page')
    else:
        page_number = 1 

    current_page = p.get_page(page_number)

    if request.user.is_authenticated:
        likes = Likes.objects.filter(message__in = current_page, user = request.user).values('message')
        posts_liked = Message.objects.filter(pk__in = likes)
    else:
        posts_liked = None

    return render(request, "network/index.html", {
        "title": "All Posts",
        "posts": current_page,
        "posts_liked": posts_liked,
        "foll": False
    })

def following(request):
    followings = Follow.objects.filter(follower = request.user).values('followed')
    posts = Message.objects.filter(user__in = followings).order_by('-date')

    p = Paginator(posts, 10) # organize posts in pages

    if request.GET.get('page') is not None:
        page_number = request.GET.get('page')
    else:
        page_number = 1 

    current_page = p.get_page(page_number)
    
    likes = Likes.objects.filter(message__in = current_page, user = request.user).values('message')
    posts_liked = Message.objects.filter(pk__in = likes)    

    return render(request, "network/index.html", {
        "title": "Following",
        "posts": current_page,
        "posts_liked": posts_liked,
        "foll": True
    })


@csrf_exempt
@login_required
def edit(request):
    if request.method == 'PUT':        
        data = json.loads(request.body)
        post_id = data["post_id"]
        if (post_id is not None):
            mes = Message.objects.get(pk = post_id)
            if mes.user == request.user:
                mes.body = data["post_body"]
                mes.save()
                return HttpResponse(status=204)
            else:
                return JsonResponse({
                    "error": "Only the post creator can edit it."
                }, status=403)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def addlike(request):
    if request.method == 'POST': 
        data = json.loads(request.body)
        post_id = data["post_id"]
        if post_id is not None:
            mes = Message.objects.get(pk = post_id)

            if mes.user != request.user:
                mes.likes += 1
                mes.save()
                lk = Likes(user = request.user, message = mes)
                lk.save()     
                return HttpResponse(status=204)
            else:
                return JsonResponse({
                    "error": "You can't put like at your own post."
                }, status=400)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

@csrf_exempt
@login_required
def remlike(request):
    if request.method == 'DELETE': 
        data = json.loads(request.body)
        post_id = data["post_id"]
        if post_id is not None:
            mes = Message.objects.get(pk = post_id)
            if mes.user != request.user:
                mes.likes -= 1
                mes.save()
                Likes.objects.filter(user = request.user, message = mes).delete()            
                return HttpResponse(status=204)
            else:
                return JsonResponse({
                    "error": "You can't remove like at your own post."
                }, status=403)
    else:
        return JsonResponse({
            "error": "DELETE request required."
        }, status=400)


def profile(request, user_id):  
    user_info = User.objects.get(pk = user_id)
    follow = 'Follow'
    if request.user != user_info:
        followed = Follow.objects.filter(follower = request.user, followed = user_id)
        if followed.count() > 0:
            follow = 'Unfollow'
        else:
            follow = 'Follow'
    return render(request, "network/profile.html", {
        "user_info": user_info,
        "posts": Message.objects.filter(user = user_info).order_by('-date'),
        "follow": follow,
        "followers": Follow.objects.filter(followed = user_info).count(),
        "following": Follow.objects.filter(follower = user_info).count()
    })


@csrf_exempt
@login_required
def follow(request):
    if request.method == 'POST':        
        data = json.loads(request.body)
        user_id = data["user_id"]
        if (user_id is not None):
            fol = Follow(follower = request.user,
                         followed = User.objects.get(pk = user_id))            
            fol.save()
            return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)


@csrf_exempt
@login_required
def unfollow(request):
    if request.method == 'DELETE':        
        data = json.loads(request.body)
        user_followed = User.objects.get(pk = data["user_id"])
        if user_followed is not None:
            Follow.objects.filter(follower = request.user, followed = user_followed).delete()            
            return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
