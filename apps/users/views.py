# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import forms as auth_forms, authenticate, login as auth_login, logout as auth_logout
from .models import *

# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request, "users/login.html")
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            auth_login(request, user)
            return redirect(index)
    return redirect(register)

@login_required(login_url=login)
def index(request):
    users = User.objects.all()
    return render(request, "users/index.html", {"users": users})

def register(request):
    if request.method == "GET":
        form = auth_forms.UserCreationForm()
        return render(request, "users/register.html", {"form": form})
    if request.method == "POST":
        form = auth_forms.UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            auth_login(request, new_user)
            return redirect(index)
        return redirect(register)

@login_required(login_url=login)
def show(request, id):
    users = User.objects.filter(id=id)
    if len(users) < 1:
        redirect(index)
    return render(request, "users/show.html", {"user": users[0]})

@login_required(login_url=login)
def edit(request):
    if request.method == "GET":
        form = UserEditForm(instance=request.user)
        return render(request, "users/edit.html", {"user": request.user, "form": form})
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect(show, id=request.user.id)

@login_required(login_url=login)
def logout(request):
    auth_logout(request)
    return redirect(login)    