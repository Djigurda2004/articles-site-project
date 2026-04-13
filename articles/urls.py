from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [
    path('',views.articles,name="articles"),
    path('addart',views.create_article,name="create"),
    path('<int:pk>',views.ArticleDetailView.as_view(),name = 'detail'),
    path('<int:pk>/edit',views.ArticleEditView.as_view(),name = 'edit'),
    path('<int:pk>/delete',views.ArticleDeleteView.as_view(),name = 'delete'),
    path('like/<int:pk>',views.like_article,name='like'),
    path('liked/',views.liked_articles,name='liked'),
]