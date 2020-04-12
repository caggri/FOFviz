from django import forms

TYPE= [
    ('fof', 'Flow of Funds'),
    ('annually', 'Balance Data Anually'),
    ('monthly', 'Balance Data Mothly')
    ]
class FileForm(forms.Form):
    file = forms.FileField() # for creating file input  
    TYPE = forms.CharField(widget=forms.RadioSelect(choices=TYPE))