from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from mail.models import *
def mark_message_as_seen(request, message_id):
    message = get_object_or_404(messages_sent, pk=message_id)
    message.seen = True
    message.save()
    return JsonResponse({'message': 'Marked as seen'})


# Create your views here.
def getcampaigns(request,ipaddress):
    campaign = Campaign.objects.filter(ip_address=ipaddress).filter(status='pending')
    if campaign:
        campaign = campaign.first()
        campaign.status = 'success'
        campaign.save()
    else:
        return JsonResponse({'status':False,'data':{}}, safe=False)
    
    emails = [mail.email for mail in EmailAudience.objects.filter(tag=campaign.tag)[:campaign.count]]
    rendered_message = render_to_string('template.html', {'message': campaign.message.content})
    campaign_data = {
            'id': campaign.id,
            'account': {"email":campaign.email.email,"password":campaign.email.apppassword,"smpt_server":campaign.email.smtp_server,"smpt_port":campaign.email.smtp_port},
            'emails': emails,
            'subject': campaign.message.subject,
            'message': rendered_message,
        }
    # Return JSON response
    return JsonResponse({'status':True,'data':campaign_data}, safe=False)

@csrf_exempt
def update_data(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body.decode('utf-8'))
            # Extract fields from the incoming data
            id = data.get('id')  # Assumed user_id is passed
            sent_from = data.get('sent_from')
            sent_to = data.get('sent_to')

            # Fetch the related User and Messages objects
            campaign = get_object_or_404(Campaign, id=id)

            # Create and save the message_sent object
            message_sent = messages_sent(
                user=campaign.user,
                message=campaign.message,
                sent_from=sent_from,
                sent_to=sent_to
            )
            message_sent.save()

            return JsonResponse({"status": "success", "message": "Message sent added successfully!"}, status=201)
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
