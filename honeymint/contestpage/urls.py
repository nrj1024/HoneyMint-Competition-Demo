from django.urls import path
from contestpage import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('invite<int:user_id>/', views.register, name='register'),
    path('invite<int:user_id>/register', views.register, name='register'),
    path('checkin', views.checkin, name='checkin'),
    path('leaderboard', views.leaderboard, name='leaderboard')    
]