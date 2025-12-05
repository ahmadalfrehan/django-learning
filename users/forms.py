from django import forms
from .models import CustomUser
class UsersForms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'