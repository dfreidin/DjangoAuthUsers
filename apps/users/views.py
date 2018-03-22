# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import forms as auth_forms, authenticate, login as auth_login, logout as auth_logout
from .models import *

# Create your views here.
def login(request):
    if request.method == "POST":
        user_pre_auth = User.objects.filter(email=request.POST["email"])
        if len(user_pre_auth) > 0:
            user = authenticate(username=user_pre_auth[0].username, password=request.POST["password"])
            if user is not None:
                messages.success(request, "Successfully logged in!")
                auth_login(request, user)
                return redirect(success)
    return redirect(index)

def index(request):
    reg_form = UserRegForm()
    log_form = LoginForm()
    return render(request, "users/index.html", {"reg_form": reg_form, "log_form": log_form})

def register(request):
    if request.method == "POST":
        form = UserRegForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            auth_login(request, new_user)
            messages.success(request, "Successfully registered!")
            return redirect(success)
        messages.error(request, form.non_field_errors())
    return redirect(index)

@login_required(login_url=index)
def success(request):
    return render(request, "users/success.html", {"user": request.user})

@login_required(login_url=login)
def edit(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect(success)
    return redirect(index)

@login_required(login_url=login)
def logout(request):
    auth_logout(request)
    return redirect(index)    