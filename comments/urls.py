from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:article_id>/',views.add_comment,name='add'),
    path('delete/<int:comment_id>/',views.delete_comment,name='delete'),
    path('edit<int:comment_id>/',views.edit_comment,name='edit'),
    path('like/<int:comment_id>/',views.like_comment,name='like'),
]