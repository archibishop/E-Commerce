from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.NotificationDetailView.as_view(),
         name='notification-item'),
    path('items', views.NotificationsView.as_view(), name='notifications-list'),
]

app_name = 'notifications'
