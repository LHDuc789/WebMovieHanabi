from django.urls import path
from . import views
app_name="accounts" #use for dynamic routing URLs

urlpatterns = [
  path('register/',views.register, name='register'),
  path('login/',views.login_user, name='login'),
  path('logout/',views.logout_user, name='logout'),
  path('detailuser/<int:id>',views.detail_user, name='detailuser'),
  path('edituser/<int:id>',views.edit_user, name='edituser'),
]