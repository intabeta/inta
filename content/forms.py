from django import forms
from django.contrib.auth.models import User


class SubmitForm(forms.Form):
    url = forms.URLField(label='URL of submission', max_length=1000)
    ig = forms.ChoiceField(label='Interest Group')
    
    def __init__(self, user, bkmk, *args, **kwargs):
        super(SubmitForm, self).__init__(*args, **kwargs)
        subscribed = []
        for ig in user.interestgroup_set.all():
            subscribed.append((ig.slug, ig.title))
        self.fields['ig'].choices = subscribed
        self.fields['url'].initial = bkmk
    

class SubmitFormPlugin(forms.Form):
    url = forms.URLField(max_length=1000)
    ig = forms.ChoiceField()
    tag = forms.CharField(max_length=100)
    
    def __init__(self, user, bkmk, *args, **kwargs):
        super(SubmitFormPlugin, self).__init__(*args, **kwargs)
        subscribed = []
        for ig in user.interestgroup_set.all():
            subscribed.append((ig.slug, ig.title))
        self.fields['ig'].choices = subscribed
        self.fields['url'].initial = bkmk
        self.fields['tag'].initial = 'Tags'

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=1000)

class SignUpForm(forms.Form):
	email = forms.EmailField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
