from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.MenuList.as_view(), name='home'),
    path('reviews', views.ReviewListView.as_view(), name='reviews'),
    path('item/<int:pk>/', views.MenuItemDetail.as_view(), name='menu_item'),
    path('about/', views.About.as_view(), name='about'),
    path('add/', views.AddItem.as_view(), name='additem'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_then_home, name='logout'),
    path('reviews/new/', views.submit_review, name='submit_review'),

]