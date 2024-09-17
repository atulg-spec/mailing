from django.urls import path
from home.views import dashboard
from mail.views import *
# urls.py
urlpatterns = [
    path("accounts",accounts,name='accounts'),
    path("delete_account/<str:id>",delete_account,name='delete_account'),
    path("account_status/<str:id>",account_status,name='account_status'),
    path("clients",clients,name='clients'),
    path("send_message",send_message,name='send_message'),
    path("upload_email_csv",upload_email_csv,name='upload_email_csv'),
    # --SINGUP AND LOGIN--
]
