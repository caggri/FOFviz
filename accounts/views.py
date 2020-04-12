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


def register(request):
    form = Register(request.POST or None)
    
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        is_ok = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

        if is_ok:
            login(request, new_user)


    return render(request, 'signup.html', {'form': form})

def profile(request):
    args = {'user':request.user}  
    return render(request, 'accounts/profile.html', args)


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