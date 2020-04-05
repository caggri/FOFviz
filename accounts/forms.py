from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class Register(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Register, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs={'class':'form-control'}
        self.fields['password'].widget=forms.PasswordInput(attrs={'class':'form-control'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def clean_email(self):
        email = self.cleaned_data['email']
        flag = len(User.objects.filter(email=email))
        if flag > 0:
            raise forms.ValidationError('This e-mail address already exist.')

        return email


class EditProfileForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        
        )

# class EditProfileForm(UserChangeForm):
#     class Meta:
#         model=User
#         fields=(
#             'email',
#             'username',
#             'instutition',
#             'full_name'
#         )

# class UserProfile(forms.ModelForm):
#     institution = forms.CharField(widget=forms.TextInput, max_length=30)
#     full_name = forms.CharField(widget=forms.TextInput, max_length=30)
#     class Meta:
#         model = User
#         fields=['username','email', 'institution', 'full_name']

#     def __init__(self, *args, **kwargs):
#         super(UserProfile, self).__init__(*args, **kwargs)

#         for field in self.fields:
#             fields[field].widgett.attrs={'class':'form-control'}

# class UserProfile(forms.ModelForm):
#     institution = forms.CharField(widget=forms.TextInput, max_length=35, label="Institution")
#     full_name = forms.CharField(widget=forms.TextInput, max_length=35, label="Full Name")
#     class Meta:
#         model = User
#         fields = ['username', 'full_name', 'institution', 'email']

#     def __init__(self, *args,  **kwargs):
#         super(UserProfile, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs={'form': 'form-control'}

