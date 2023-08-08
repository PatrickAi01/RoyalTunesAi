from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from websets.models import Customer
from django.core.validators import FileExtensionValidator


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'  # or specify the specific fields you want to include in the form

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class audioAccept(forms.Form):
    audioFile = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])])
        
