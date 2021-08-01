from .views import index,Signup,Login
from django.urls import path,include
urlpatterns = [
    path('', index, name='homepage'),
    path('signup' , Signup.as_view()),
    path('login', Login.as_view())
]