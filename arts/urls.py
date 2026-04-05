from django.urls import path
from . import views


app_name = 'arts'
urlpatterns = [
    path('',views.arts,name="arts"),
    path('addart',views.add_art,name="add"),
    path('<int:pk>',views.ArtDetailView.as_view(),name = 'detail'),
    path('<int:pk>/edit',views.ArtEditView.as_view(),name = 'edit'),
    path('<int:pk>/delete',views.ArtDeleteView.as_view(),name = 'delete'),
    path('like/<int:pk>',views.like_article,name='like'),
    path('liked/',views.liked_articles,name='liked'),
]