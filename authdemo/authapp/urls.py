from django.urls import path
from . import views
urlpatterns =[
   path('',views.index,name='home'),
   path('signup/',views.signup,name='signup'),
   path('login',views.login_view,name='login'),
   path('change-password/',views.change_pasword,name='change-password'),
   path('change-profile/',views.change_profile,name='change-profile'),
   path('delete-account/',views.delete_account, name='delete-account'),
   path('signout/',views.signout,name='signout'),

]