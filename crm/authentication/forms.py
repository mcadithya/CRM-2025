from django import forms
from django.contrib.auth.models import User
class LoginForm(forms.Form):

    email = forms.EmailField( widget= forms.EmailInput(attrs={'class':'form-select','required':'required'}))

    password= forms.CharField(max_length=5,widget=forms.PasswordInput(attrs={'class':'form-select','required':'required'}))

def clean(self):

        cleaned_data =  super().clean()

        email = cleaned_data.get('email')

        username, domian = email.split('@')

        doamin_list = ["gmail.com",
                        "yahoo.com",
                        "outlook.com",
                        "hotmail.com",
                        "icloud.com",
                        "aol.com",
                        "protonmail.com",
                        "zoho.com",
                        "yandex.com",
                        "mail.com"]
        if domian not in doamin_list:

            self.add_error('email','Invalid email address')
        
        if not User.objects.filter(username=email).exists():
             
             self.add_error('email','not registered email')

