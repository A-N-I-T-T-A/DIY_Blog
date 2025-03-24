from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('blog/<int:pk>/create/', views.CommentCreate.as_view(), name='comment-create'),
    path('register/', views.register, name='register'),
    path('blog/create/', views.BlogCreate.as_view(), name='blog-create'),
    path('blog/<int:pk>/update/', views.BlogUpdate.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', views.BlogDelete.as_view(), name='blog-delete'),
    path('blogger/<int:pk>/update/', views.BloggerUpdate.as_view(), name='blogger-update'),
    path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment-delete'),
    path('profile/<int:pk>/', views.BloggerDetailView.as_view(), name='user-profile'),
] 