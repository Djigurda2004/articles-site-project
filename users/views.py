from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.conf import settings
from django.http import HttpResponseForbidden
from .forms import ProfileForm
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})


def profile_detail(request,username):
    user = get_object_or_404(User,username=username)
    profile = user.profile
    articles = user.articles.all()
    return render(request, "users/profile_detail.html",{"profile":profile,"articles":articles})


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("users:profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "users/profile_edit.html", {"form": form})


@login_required
def follow_user(request,username):
    user = get_object_or_404(User,username=username)
    profile= user.profile
    if request.user == profile.user:
        return HttpResponseForbidden()
    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
    if request.headers.get('HX-Request'):
        return render(request,'users/follow_area.html',{'profile':profile})
    return redirect("users:profile",username=username)


@login_required
def following_user(request):
    following = request.user.following.all().select_related("user").prefetch_related("followers")
    return render(request,"users/following.html",{"following":following})