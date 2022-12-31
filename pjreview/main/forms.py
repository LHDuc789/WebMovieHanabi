from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'director', 'cast', 'description', 'release_date', 'image')
        
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment','rating')