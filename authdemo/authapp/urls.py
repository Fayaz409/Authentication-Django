from django.urls import path
from . import views
urlpatterns =[
   path('',views.index,name='home'),
   path('signup/',views.signup,name='signup'),
   path('login',views.login_view,name='login'),
   path('change-password/',views.change_pasword,name='change-password'),
]