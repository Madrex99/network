from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .models import User, Posts, Follow, Likes


def index(request):
    tweets = Posts.objects.all()
    p = Paginator(tweets, 10)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    # Convert likes to a list for easy checking in the template
    likes = list(Likes.objects.filter(user=request.user).values_list('post_id', flat=True))

    return render(request, "network/index.html", {
        "pages": page_obj,
        "likes": likes
    })


@csrf_exempt
def edit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    text = data.get("text", "")
    post_id = data.get("id")
    print(text)
    
    # Get the post and update it
    try:
        post = Posts.objects.get(id=post_id)
        print(post)
        post.text = text
        post.save()
        return JsonResponse({"message": "The post has been successfully edited."}, status=201)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    

def post(request):
    if request.method == "POST":
        tweet = request.POST['text']
        user = User.objects.get(pk=request.user.id)
        post = Posts(text=tweet, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))
    
def profile(request, profile_id):
    user = User.objects.get(pk=profile_id)
    tweets = Posts.objects.filter(user=user).order_by("date").reverse()

    followers = user.followed.count()
    following = user.follower.count()

    if profile_id != request.user.id:
        button = "yes"
    else:
        button = "no"

    if Follow.objects.filter(user=request.user, user_followed=user):
        follow = "yes"
    else:
        follow = "no"
    
    p = Paginator(tweets, 10)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/profile.html", {
        "followers": followers,
        "following": following,
        "user": user,
        "button": button,
        "follow": follow,
        "pages": page_obj
    })

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


def follow(request, profile_id):
    if request.method == "POST":
        profile = User.objects.get(pk=profile_id)
        data = Follow(
            user = request.user,
            user_followed = profile
        )
        data.save()

        return HttpResponseRedirect(reverse('profile', args=[profile_id]))


def unfollow(request, profile_id):
    if request.method == "POST":
        profile = User.objects.get(pk=profile_id)
        data = Follow.objects.filter(user=request.user, user_followed=profile)
        data.delete()

        return HttpResponseRedirect(reverse('profile', args=[profile_id]))
    

def following(request):
    user = request.user
    following_users = Follow.objects.filter(user_followed=user).values_list('user', flat=True)
    tweets = Posts.objects.filter(user__in=following_users).order_by("date").reverse()
    
    p = Paginator(tweets, 10)

    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/following.html", {
        "pages": page_obj
    })


@csrf_exempt
def unlike_post(request, post_id):
    post = Posts.objects.get(pk=post_id)
    post.likes -= 1
    user = User.objects.get(pk=request.user.id)
    like = Likes.objects.filter(user=user, post=post)
    like.delete()
    post.save()
    return JsonResponse({"message": "Like removed!", "likes": post.likes})

@csrf_exempt
def like_post(request, post_id):
    post = Posts.objects.get(pk=post_id)
    post.likes += 1
    user = User.objects.get(pk=request.user.id)
    newLike = Likes(user=user, post=post)
    newLike.save()
    post.save()
    return JsonResponse({"message": "Like added!", "likes": post.likes})