# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('mark_as_seen/<int:message_id>/', views.mark_message_as_seen, name='mark_message_as_seen'),
    # Other paths in your urlpatterns
]
