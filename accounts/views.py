# accounts/views.py
# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic
# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import Register
from django.contrib.auth import authenticate, login
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

# class SignUp(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'


# def signup_view(request):
#     form = SignUpForm(request.POST)
#     if form.is_valid():
#         form.save()
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         return redirect('home')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(request, _('Your password was successfully updated!'))
#             return redirect('registration:password_change_form')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'registration/password_change_form.html', {
#         'form': form
#     })

# def edit_profile(request):
#     if request.method == 'POST':
#         form = UserChangeForm(request.POST, instance=request.user)

#         if form.is_valid():
#             form.save()
#             return redirect('/')

#     else:
#         form = UserChangeForm(instance=request.user)
#         args = {'form': form}
#         return render('accounts/edit_profile.html', args)