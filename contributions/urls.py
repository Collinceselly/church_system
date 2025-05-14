from django.urls import path
from . import views

urlpatterns = [
    path('member/<int:member_id>/add/', views.add_contribution, name='add_contribution'),
    path('member/<int:member_id>/contributions/', views.member_contributions, name='member_contributions'),
    path('individual/<int:member_id>/', views.individual_contributions, name = 'individual_contributions'),
    path('all/contributions/', views.all_contributions, name='all_contributions'),
]