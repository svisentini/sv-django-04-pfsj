from django import forms
from .models import Joia

class JoiaForm(forms.ModelForm):
    class Meta:
        model = Joia
        fields = '__all__'
