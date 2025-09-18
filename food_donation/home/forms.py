from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm
from django.contrib.auth import password_validation

class UserRegistration(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password','autofocus': False}))

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password Again','autofocus': False}))
    class Meta:
        model=User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {

            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter First Name','autofocus': False}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name','autofocus': False}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username','autofocus': False}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email ID','autofocus': False})
        }

class DonorSignupForm(forms.ModelForm):
    profilepic = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class':'form-control','autofocus': False}))    
    class Meta:
        model=Donor
        fields = ['contact','profilepic', 'address']
        widgets={
            'contact': forms.NumberInput(attrs={'class':'form-control','placeholder':'Contact Number','autofocus': False}),
            'address': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Address','autofocus': False})
        }


class StaffSignupForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['contact', 'profilepic', 'idpic', 'address', 'about']
        widgets = {
            'contact': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Contact Number',
                'autofocus': False
            }),
            'profilepic': forms.FileInput(attrs={
                'class': 'form-control',
                'autofocus': False
            }),
            'idpic': forms.FileInput(attrs={
                'class': 'form-control',
                'autofocus': False
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Address',
                'autofocus': False
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'About',
                'autofocus': False
            }),
        }


class ChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class':'form-control', 'placeholder': 'Old Password'}))

    new_password1 = forms.CharField(label='New Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',  'class':'form-control', 'placeholder': 'New Password'}), help_text=password_validation.password_validators_help_text_html())  

    new_password2 = forms.CharField(label='Confirm New Password', strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',  'class':'form-control', 'placeholder': 'Confirm Password'}))     

class ForgotPassword(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))    

class DonateNowForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['item_name', 'item_pic', 'location', 'description']    
        widgets = {
            'item_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Food Item Name'}),
            'location': forms.Select(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
            'item_pic': forms.FileInput(attrs={'class':'form-control'}),
        }
        labels = {
            'item_pic':'Donation Image (Picture of the Food)',
            'item_name':'Food Item Name',
            'location': 'Donation Location',
            'description':'Description',
        }

class DonationAreaForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name','description']
        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Donation Area'}),
            'description':forms.TextInput(attrs={'class':'form-control','placeholder':'Description'})
        }
        labels={
            'name':'Donation Area Name',
            'description':'Description'
        }