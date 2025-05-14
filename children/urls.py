from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_child, name='add_child'),
    path('all/', views.all_children, name='children_list'),
    path('validate_parent/<str:unique_id>/', views.validate_parent, name='validate_parent'),
]