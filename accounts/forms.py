from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
# class SignUpForm(UserCreationForm):
#     username = forms.CharField(max_length=30)
#     # email = forms.EmailField(max_length=200)
#     # email2 = forms.CharField(max_length=200)

#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', )

