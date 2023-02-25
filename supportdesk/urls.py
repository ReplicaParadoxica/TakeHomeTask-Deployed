from django.urls import path
from .views import (
    HomeView,
    RequestListView,
    RequestCreateView,
    RequestDetailView,
    mark_request_completed,
    reassign_request,
)

urlpatterns = [
    path("placeholder/", HomeView.as_view(),
         name="supportdesk_placeholder"),
    path('', RequestListView.as_view(), name='request_list'),
    path('support/', RequestCreateView.as_view(), name='new_request'),
    path('mytickets/<str:pk>/', RequestDetailView.as_view(),
         name='request_detail'),
    path('oldticket/<str:pk>/', mark_request_completed, name='mark_completed'),
    path('reassign/<str:requestID>/<str:agentID>',
         reassign_request, name='reassign_agent'),
]
