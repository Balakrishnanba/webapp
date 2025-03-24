from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upload/', views.upload_image, name='upload'),
    path('send_email/', views.send_image_email, name='send_email'),
    path('verify_qr/', views.verify_qr, name='verify_qr'),
    path('email_history/', views.email_history, name='email_history'),
    path('delete_key/<int:key_id>/', views.delete_key, name='delete_key'),

   
]