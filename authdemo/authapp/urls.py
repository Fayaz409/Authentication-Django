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
   path('roles-list/',views.roles_list,name='roles-list'),
   path('create-role/',views.create_role,name='create-role'),
   path('update-role/<str:name>',views.edit_role,name='update-role'),
   path('delete-group/<int:role_id>',views.delete_role,name='delete-group'),
   path('all-staff/',views.staff_list,name='all-staff'),
   path('staff-list/',views.staff_list,name='staff-list'),
   path('create-staff-employee/',views.create_staff_employee,name='create-staff-employee'),
]