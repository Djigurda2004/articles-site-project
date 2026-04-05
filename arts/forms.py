from .models import Articles
from django.forms import ModelForm,TextInput,Textarea

class ArticlesForm(ModelForm):
    class Meta:
        model =  Articles
        fields = ['title','anons','full_text']
        widgets ={
            "title": TextInput(attrs={'class': 'form-control','placeholder':'Article title'}),
            "anons": TextInput(attrs={'class': 'form-control','placeholder':'Article announcement'}),
            "full_text" : Textarea(attrs={'class': 'form-control','placeholder' : 'Article content'})
        }