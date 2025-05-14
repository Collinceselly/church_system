from django.urls import path
from .views import (MembersListView,
                     MembersDetailView,
                     MembersCreateView,
                    MembersUpdateView, 
                    MembersDeleteView, 
                    MoreMembersDetailView, 
                    IndividualMemberDetailView, 
                    IndividualMemberMoreDetailView)
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('members/new/', MembersCreateView.as_view(), name = 'member_create'),
    path('members/all/', MembersListView.as_view(), name='members_all'),
    path('member/me/', MembersDetailView.as_view(), name='member_detail'),
    path('member/<int:pk>/more/', MoreMembersDetailView.as_view(), name='member_more_detail'),
    path('member/<int:pk>/update/', MembersUpdateView.as_view(), name='member_update'),
    path('member/<int:pk>/delete/', MembersDeleteView.as_view(), name='member_delete'),
    path('individual/member/<int:pk>', IndividualMemberDetailView.as_view(), name='individual_member'),
    path('individual/member/<int:pk>/more/', IndividualMemberMoreDetailView.as_view(), name='individual_member_more'),
    path('about/', views.about, name='members_about')
]