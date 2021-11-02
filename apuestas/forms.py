from django import forms

class LoginMiniForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required = True)
    password = forms.CharField(label='Password', max_length=50, required = True, widget = forms.PasswordInput())
    
class LogoutMiniForm(forms.Form):
    username = forms.CharField(label='logout', max_length=50, required = False, widget = forms.HiddenInput())
    
