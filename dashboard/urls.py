# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("getcampaigns/<str:ipaddress>",views.getcampaigns,name='getcampaigns'),
    path('mark_as_seen/<int:message_id>/', views.mark_message_as_seen, name='mark_message_as_seen'),
    path('update-data', views.update_data, name='update_data'),
    # Other paths in your urlpatterns
]
