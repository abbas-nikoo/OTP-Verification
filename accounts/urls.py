from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('verify/', views.UserOtpCode.as_view(), name='verify'),
    path('home/', views.Home.as_view(), name='home'),
    path('retrieve/<slug:slug_id>/', views.PostRetrivView.as_view()),
    path('create/', views.PostCreateView.as_view()),
    path('update/<slug:slug_id>/', views.PostUpdateView.as_view()),
    path('delete/<slug:slug_id>/', views.PostDeleteView.as_view()),
]
