from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Nguoidung
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control",
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))



class NguoidungForm(forms.ModelForm):
    gioitinh=forms.ChoiceField(
            widget=forms.RadioSelect(attrs={'class':'form-check-label'}),
            choices=[
                    ('nam', 'Nam'),
                    ('nữ', 'Nữ'),
                    ]
                    
        )
    class Meta:
        model = Nguoidung
        fields = [
            'ho',
            'ten',
            'gioitinh',
            'ngaysinh',
            'sdt',
            'email'
        ]
        widgets= {
            'ho': forms.TextInput(attrs={'class':'form-control'}),
            'ten': forms.TextInput(attrs={'class':'form-control'}),
            'ngaysinh': forms.DateInput(attrs={'class':'form-control','id':'ngaysinh'}),
            'sdt': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'})
        }

class FormChangepass(forms.Form):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Your Password",
                "class": "form-control"
            }
        ))
    password1= forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password",
                "class": "form-control"
            }
        ))