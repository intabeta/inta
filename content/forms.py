from django import forms
from django.contrib.auth.models import User


class SubmitForm(forms.Form):
    url = forms.URLField(label='URL of submission', max_length=1000)
    
    def __init__(self, user, bkmk, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        subscribed = []
        self.fields['url'].initial = bkmk
    

class SubmitFormPlugin(forms.Form):
    url = forms.URLField(max_length=1000)
    tags = forms.CharField(max_length=100)
    
    def __init__(self, user, bkmk, inittags, *args, **kwargs):
        super(SubmitFormPlugin, self).__init__(*args, **kwargs)
        subscribed = []
        self.fields['url'].initial = bkmk
        self.fields['tags'].initial = inittags

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=1000)

class SignUpForm(forms.Form):
	email = forms.EmailField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
