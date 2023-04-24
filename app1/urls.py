from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.registerUser,name="registerUser"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('add_project/',views.add_pro,name="add_pro"),
    path('add_projects/',views.add_projects,name="add_projects"),
    path('profile/<str:uname>/',views.profile,name="profile"),
    path('userlist/',views.userlist,name="userlist"),
    path('delete/<int:id>/<str:uname>/',views.delete,name="delete"),
    path('update_to/<int:id>/<str:uname>/',views.update_to,name="update_to"),
    path('update/<int:id>/<str:uname>/',views.update,name="update"),
    
    
]