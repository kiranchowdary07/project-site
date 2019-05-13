from django.urls import path

from . import views
from mysite.views import create
from mysite.views import profile_index
from mysite.views import profile_detail
from mysite.views import edit_profile

app_name='mysite'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:id>/update/',views.update, name='update'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('profile/', views.profile_index, name='profile_index'),
    path('profile/<int:id>/', views.profile_detail, name='profile_detail'),
    path('plans/', views.plans_view, name='plan_view')



]
