from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Comments, Auction, Bids, Watchlist
from django.db.models import Max, Count
from datetime import datetime
from django.contrib.auth.decorators import login_required


def index(request):
    Auction.objects.filter(deadline__lte = datetime.now()).update(closed = True)
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(closed = False).order_by('-deadline')
    })


def show_cat_listings(request, category):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(category = category)
    })


def show_categories(request):
    return render(request, "auctions/categories.html", {
        "cats": Auction.objects.values('category').filter(closed = False).annotate(auc = Count('category'))
    })

@login_required
def show_watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "auctions": Watchlist.objects.filter(watcher = request.user)
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        auc = Auction(title = request.POST["title"],
                      description = request.POST['description'],
                      category = request.POST['category'], 
                      best_bid = request.POST['start'],                                      
                      deadline = request.POST['deadline'],
                      image_addr = request.POST['imageaddr'],
                      seller = request.user)
        auc.save()
        bid = Bids(bid = request.POST['start'],
                   bidder = request.user,
                   auction = auc)
        bid.save()        
        return HttpResponseRedirect(f"listing/{auc.pk}")
    else:    
        return render(request, "auctions/create.html")


def show_listing(request, item):
    listing = Auction.objects.get(pk = item)
    if listing:
        bid_button = False   
        best_bid = listing.best_bid
        if listing.closed:
            bid = Bids.objects.filter(auction__pk = item).order_by('-bid').first()
            if (bid.bidder == request.user) and (request.user != listing.seller):
                messagec = "You Win"
                messagec_type = "success"
            else:
                messagec = "Auction Closed"
                messagec_type = "danger"

            return render(request, "auctions/listing.html", { 
                "listing": listing,                
                "messagec": messagec,
                "messagec_type": messagec_type,
                "bid_button": bid_button
            })  
        else: 
            resultadd = ["", ""]
            resultwatch = ["", ""]            

            if request.user.is_authenticated:
                try:
                    Watchlist.objects.get(watcher = request.user, auction = listing)
                    resultwatch = ["Remove from watchlist", "danger"]
                except Watchlist.DoesNotExist:
                    resultwatch = ["Add to watchlist", "success"]

                bid_button = False if request.user == listing.seller else True  
                if request.method == "POST":
                    if request.POST['type'] == "addbid":
                        resultadd = add_bid(request, listing)
                        listing = Auction.objects.get(pk = item)                        
                    elif request.POST['type'] == "addremtow":
                        resultwatch = addrem_to_watchlist(request, listing)
                    elif request.POST['type'] == "close":
                        close_auction(item)
                        listing = Auction.objects.get(pk = item)
                    elif request.POST['type'] == "comment":
                        add_comment(request, listing)  

            return render(request, "auctions/listing.html", { 
                "listing": listing,
                "tot_bid": Bids.objects.filter(auction__pk = item).aggregate(Count('bid'))   ,
                "comments": Comments.objects.filter(auction__pk = item).order_by('-date'),
                "message": resultadd[0],
                "message_type": resultadd[1],
                "messagew": resultwatch[0],
                "messagew_type": resultwatch[1],
                "bid_button": bid_button
            })    
    else:
        return render(request, "auctions/listing.html", {
            "message": "No listings with this Id",
            "message_type": "danger"
        })

@login_required
def add_bid(request, listing): 
    if request.user != listing.seller:                
        if int(request.POST['bid']) > listing.best_bid: # new bid is grater than the actual one
            bid = Bids(bid = request.POST['bid'],
                       bidder = request.user,
                       auction = listing)
            bid.save()
            Auction.objects.filter(pk = listing.pk).update(best_bid = request.POST['bid'])
            message = "Your bid has been saved"
            message_type = "success"                    
        else:                    
            message = "Your bid is not enough"
            message_type = "warning"                    
    else:
        message = "Seller can't place bids" 
        message_type = "warning" 

    return message, message_type   

@login_required
def addrem_to_watchlist(request, listing):
    try:
        Watchlist.objects.get(watcher = request.user, auction = listing).delete()
        messagew = "Add to watchlist"
        messagew_type = "success"
    except Watchlist.DoesNotExist:
        Watchlist(watcher = request.user, auction = listing).save()     
        messagew = "Remove from watchlist"
        messagew_type = "danger"

    return messagew, messagew_type


def close_auction(item):    
    return Auction.objects.filter(pk = item).update(closed = True)

@login_required
def add_comment(request, listing):
    return Comments(title = request.POST["title"],
                    content = request.POST["content"],
                    auction = listing).save() 


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
