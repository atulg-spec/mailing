from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import messages_sent

def mark_message_as_seen(request, message_id):
    message = get_object_or_404(messages_sent, pk=message_id)
    message.seen = True
    message.save()
    return JsonResponse({'message': 'Marked as seen'})
