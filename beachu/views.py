import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import User, Estabs, Favourite, Comment, Booking
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import F
import datetime
from django.db import IntegrityError

# Create your views here.

def index(request): 
    return render(request, "beachu/index.html", {
        "home_active": "active"
    })

# Add a new establishment to the db
@login_required
def insertnew(request):
    if request.user.is_authenticated and request.user.is_manager:
        if request.method == 'POST':
            estab = Estabs(name = request.POST["name"],
                        street = request.POST["street"],
                        number = request.POST["number"],
                        city = request.POST["city"],
                        zipcode = request.POST["zipcode"],
                        country = request.POST["country"],
                        phone = request.POST["phone"],
                        available = request.POST["available"],
                        umbrellas = request.POST["umbrellas"],
                        manager = request.user)
            estab.save()      
            return redirect('estabpage', estabid=estab.pk)

        return render(request, "beachu/insertnew.html", {
            "insert_active": "active"
        })
    else:
        return render(request, "beachu/index.html", {
            "home_active": "active"
        })


# Page of one establishment
def estabpage(request, estabid):
    if request.method == 'GET':
        estab = Estabs.objects.get(pk = estabid)

        bookimg = '/static/beachu/images/calendar-check.svg'
        booktext = "Book your place now!"
        bookinput = 'block'
        booked_dis = 'none'
        booked_cont = 0
        favimg = '/static/beachu/images/suit-heart.svg'
        favtext = "Add to favourites!" 
        
        if estab.manager != request.user and request.user.is_authenticated:
            try:
                book = Booking.objects.get(estab = estab, booker = request.user)
            except:
                book = None

            fav = Favourite.objects.filter(favestab = estab, favuser = request.user).count() 

            if book: # Booking
                bookimg = '/static/beachu/images/calendar-check-fill.svg'
                booktext = "Remove your booking" 
                bookinput = 'none'      
                booked_dis = 'block'  
                booked_cont = book.umb  
            if fav > 0: # Fav
                    favimg = '/static/beachu/images/suit-heart-fill.svg'
                    favtext = "Remove from favourites"
                            

        # Comments
        posts = Comment.objects.filter(estab = estab).order_by('-date')
    
        p = Paginator(posts, 5) # organize posts in pages

        if request.GET.get('page') is not None:
            page_number = request.GET.get('page')
        else:
            page_number = 1 

        current_page = p.get_page(page_number)       

        return render(request, "beachu/estabpage.html", {
            "estab": estab,
            "posts": current_page,
            "bookimg": bookimg,
            "booktext": booktext,
            "nrumb": bookinput,
            "booked_dis": booked_dis,
            "booked_cont": booked_cont,
            "favimg": favimg,
            "favtext": favtext,
            "list_active": "active"
        })
    else: 
        return render(request, "beachu/index.html", {
            "home_active": "active"
        })    


@csrf_exempt
@login_required
def addcomment(request):
    if request.method == "POST":  
        data = json.loads(request.body)      
        mes = Comment(estab = Estabs.objects.get(pk = data['estab_id']),
                      body = data["textpost"],
                      user = request.user)
        mes.save()    
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "POST request is required"
        }, status=400)


@csrf_exempt
@login_required
def editcomment(request):
    if request.method == "PUT":
        data = json.loads(request.body)    
        Comment.objects.filter(pk = data["post_id"], user = request.user).update(body = data["post_body"]) 
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request is required"
        }, status=400)


# Page with the user manager's establishments list
def establist(request):    
    estabs = Estabs.objects.filter(manager = request.user)

    return render(request, "beachu/establist.html", {
        "list_active": 'active',
        "estabs": estabs,
        "is_list": True
    })


def estabfav(request):
    favs = Favourite.objects.filter(favuser = request.user).values('favestab')
  
    return render(request, "beachu/establist.html", {        
        "fav_active": 'active',
        "estabs": Estabs.objects.filter(pk__in = favs.values('favestab')),
        "is_list": False
    })


def estabook(request):   
    books = Booking.objects.filter(booker = request.user)

    return render(request, "beachu/establist.html", {
        "book_active": 'active',
        "estabs": Estabs.objects.filter(pk__in = books.values('estab')),
        "is_list": False
    })

@csrf_exempt
@login_required
def addbook(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        estab_id = data["estab_id"]
        if estab_id is not None:
            estab = Estabs.objects.get(pk = estab_id)
            if estab.manager != request.user:
                start_date = datetime.date.today() + datetime.timedelta(days=1)
                end_date = datetime.date.today() + datetime.timedelta(days=2)                
                book = Booking.objects.filter(estab = estab, 
                                              booker = request.user,
                                              date__range = (start_date, end_date)).count()
                if book == 0:
                    newbook = Booking(estab = estab, booker = request.user)
                    newbook.save()
                    return HttpResponse(status=204)
                else:
                    return JsonResponse({
                        "error": "Booking already exists"
                    }, status=400)
            else:
                return JsonResponse({
                        "error": "You can't book in your own establishment"
                    }, status=400)
    else:
        return JsonResponse({
            "error": "POST request is required"
        }, status=400)

@csrf_exempt
@login_required
def rembook(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)  
        estab_id = data["estab_id"]
        if estab_id is not None:
            estab = Estabs.objects.get(pk = estab_id)
            book = Booking.objects.filter(estab = estab, booker = request.user).delete()
            if book:
                return HttpResponse(status=204)
            else:
                return HttpResponse(status=500)
        else:
            return HttpResponse(status=400)
    else:
        return JsonResponse({
            "error": "DELETE request is required"
        }, status=400)


# Page with which user looks for establishments
@csrf_exempt
def estabsearch(request):
    if request.method == 'GET':
        place = request.GET.get("place")
        zipcode = request.GET.get("zipcode")
        estabs = Estabs.objects.filter(city = place, zipcode = zipcode)
    else:
        estabs = None    

    return render(request, "beachu/establist.html", {
        "list_active": "",
        "estabs": estabs
    })


# Add a record with favourite establishments infos
@csrf_exempt
@login_required
def addfav(request):
    if request.method == 'POST': 
        data = json.loads(request.body)
        estab_id = data["estab_id"]
        if estab_id is not None:
            estab = Estabs.objects.get(pk = estab_id)
            if estab.manager != request.user:
                fav = Favourite(favuser = request.user, favestab = estab)
                fav.save()     
                return HttpResponse(status=204)
            else:
                return JsonResponse({
                    "error": "You can't fav your own esatblishment."
                }, status=406)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)


# Remove a record with favourite establishments infos
@csrf_exempt
@login_required
def remfav(request):
    if request.method == 'DELETE': 
        data = json.loads(request.body)
        estab_id = data["estab_id"]
        if estab_id is not None:
            estab = Estabs.objects.get(pk = estab_id)
            if estab.manager != request.user:
                fav = Favourite.objects.filter(favuser = request.user, favestab = estab).delete()
                return HttpResponse(status=204)
            else:
                return JsonResponse({
                    "error": "You can't unfav your own esatblishment."
                }, status=400)
    else:
        return JsonResponse({
            "error": "DELETE request required."
        }, status=400)


@csrf_exempt
@login_required
def increaseUmb(request):
    if request.method == 'PUT' and request.user.is_manager: 
        data = json.loads(request.body)
        estab_id = data["estab_id"]
        if estab_id is not None:
            estab = Estabs.objects.get(pk = estab_id)
            if estab.available < estab.umbrellas:
                Estabs.objects.filter(pk = estab_id).update(available = F('available') + 1)
                return HttpResponse(status=204)
            else:
                return JsonResponse({
                    "error": "You can't increase them more"
                    }, status=401)
        else:
            return JsonResponse({
                "error": "Something was wrong"
                }, status=400)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=405)

@csrf_exempt
@login_required
def decreaseUmb(request):
    if request.method == 'PUT' and request.user.is_manager: 
        data = json.loads(request.body)
        estab_id = data["estab_id"]
        if estab_id is not None:
            estab = Estabs.objects.get(pk = estab_id)
            if estab.available > 0:
                Estabs.objects.filter(pk = estab_id).update(available = F('available') - 1)
                return HttpResponse(status=204)
            else:
                return JsonResponse({
                    "error": "You can't decrease them more"
                    }, status=401)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=405)

# Login management
@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "beachu/index.html", {
                "login_active": "active",
                "message": "Invalid username and/or password."
            })            


# Logout management
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST.get("email")
        manager = True if request.POST.get("manager") == 'on' else False

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "beachu/index.html", {
                "reg_active": "active",
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, is_manager = manager)
            user.save()
        except IntegrityError:
            return render(request, "beachu/index.html", {
                "reg_active": "active",
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "beachu/index.html", {
            "reg_active": "active",
        })