from django import forms

class Signup(forms.Form):
    Username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    Email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))

class Login(forms.Form):
    Username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

class Update(forms.Form):
    def __init__(self, *args, **kwargs):
        username = kwargs.pop('username', '')
        email = kwargs.pop('email', '')
        super(Update, self).__init__(*args, **kwargs)
        self.fields["Username"].widget.attrs['value'] = username
        self.fields["Email"].widget.attrs['value'] = email

    Username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control', 'readonly' : 'readonly'}))
    Password = forms.CharField(required = False, widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    Email = forms.EmailField(required = False, max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))