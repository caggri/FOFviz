# accounts/views.py
# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic
# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.ofile/forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import Register, EditProfileForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django import forms

#This entire page utilize django auth rules

#This function helps register the user
def register(request):
    form = Register(request.POST or None)
    
    #determine user name and password and login
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        #to determine if the password meets the minimum length requirement
        passwd_len =len(str(form.cleaned_data['password']))
        print(passwd_len)
        
        #registering the user and authenticating them    
        new_user.save()
        is_ok = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

        if is_ok:
            login(request, new_user)


    return render(request, 'signup.html', {'form': form})

#display user profile
def profile(request):
    args = {'user':request.user}  
    return render(request, 'accounts/profile.html', args)


#Make changes like user-name and user-image
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

#To allow the user to change their password
#utilizes django built in auth features
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
    
        else:
            form = PasswordChangeForm(data = request.POST, user=request.user)
            args={'form':form}
            return render(request, 'accounts/change_password.html', args)
    else:
        form = PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request, 'accounts/change_password.html', args)