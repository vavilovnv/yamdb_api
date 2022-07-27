from django.forms import ModelForm

from .models import CustomUser


class UserForm(ModelForm):
    model = CustomUser
