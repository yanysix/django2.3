from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.indexacc, name='profile'),
    path('account/filter/', views.indexacc_filter, name='profile_filter'),
    path('signup/', views.signup, name='signup'),
    path('request/add/', request_add, name="request_add"),
    path('request/delete/<int:pk>/', request_delete, name="request_delete"),
    path('request/delete/confirm/<int:pk>/', request_delete_confirm, name="request_delete_confirm"),
    path('request/', requests, name="requests"),
    path('request/work/change/<int:pk>/', request_work_change, name="request_work_change"),
    path('request/done/change/<int:pk>/', request_done_change, name="request_done_change"),

]
