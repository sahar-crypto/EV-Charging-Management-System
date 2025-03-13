from django import forms
from api.models import Station, Charger
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'location']

class ChargerForm(forms.ModelForm):
    class Meta:
        model = Charger
        fields = ['charger_id', 'model', 'vendor']

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    is_staff = forms.BooleanField(label='Are you an admin?', required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'is_staff', 'password1', 'password2']  # Fixed

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')  # Fixed
