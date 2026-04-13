from .models import Article
from django.forms import ModelForm,TextInput,Textarea

class ArticleForm(ModelForm):
    class Meta:
        model =  Article
        fields = ['title','announcement','full_text']
        widgets ={
            "title": TextInput(attrs={'class': 'form-control','placeholder':'Article title'}),
            "announcement": TextInput(attrs={'class': 'form-control','placeholder':'Article announcement'}),
            "full_text" : Textarea(attrs={'class': 'form-control','placeholder' : 'Article content'})
        }