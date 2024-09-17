from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from dashboard.models import *
from mail.models import *
from mail.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import threading
from mail.messaging.sendmessage import send_bulk_emails
from django.core.paginator import Paginator
from django.db.models import Count


# Create your views here.
User = get_user_model()

# -=--------=---=----------=--=------PAGES--=---=------=---
# HOME
@login_required
def accounts(request):
    if request.method == 'POST':
        form = Email_account(request.POST)
        if form.is_valid():
            try:
                ac = form.save(commit=False)
                ac.user = request.user
                ac.save()
                messages.success(request,'Account Added Successfully.')
            except ValidationError as e:
                messages.error(request, e)
        else:
            messages.error(request,form.errors)
    acc = EmailAccounts.objects.filter(user=request.user)
    context = {
        'acc':acc,
    }
    return redirect('/mail/clients')

@login_required
def delete_account(request,id):
    acc = EmailAccounts.objects.filter(id = id).first()
    if acc.user != request.user:
        return redirect('/mail/clients')
    acc.user = User.objects.get(email='admin@gmail.com')
    acc.save()
    messages.success(request,"Account deleted successfully")
    return redirect("/mail/clients")

@login_required
def account_status(request,id):
    acc = EmailAccounts.objects.filter(id = id).first()
    if acc.user != request.user:
        return redirect('/email/clients')
    if acc.is_active:
        acc.is_active = False
        acc.save()
    else:
        acc.is_active = True
        acc.save()
    messages.success(request,"Email Account status Updated !")
    return redirect("/mail/clients")


@login_required
def upload_email_csv(request):
    if request.method == 'POST':
        form = EmailClientDataForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request, "Successfully uploaded data.")
            return redirect("/mail/clients")
        else:
            messages.error(request, "Invalid file or Invallid data fields.")
            return redirect("/mail/clients")  # Redirect if the form is invalid
    else:
        form = EmailClientDataForm()
    
    return redirect('/mail/clients')


@login_required
def clients(request):
    if request.method == 'POST':
        form = Client_email(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request,'Client Added Successfully.')
        else:
            messages.error(request,'Something went wrong ! Please try again later.')
        return redirect('/mail/clients')
    aud = EmailAudience.objects.filter(user=request.user)
    tagz = list(EmailAudience.objects.filter(user=request.user).values('tag').annotate(count=Count('tag')).values_list('tag', flat=True))
    paginator = Paginator(aud,10)
    page_number=request.GET.get('page')
    aud_final = paginator.get_page(page_number)
    csvform = EmailClientDataForm()
    msgs = Messages.objects.filter(user=request.user)
    acc = EmailAccounts.objects.filter(user=request.user)
    context = {
        'tagz':tagz,
        'aud':aud_final,
        'msgs':msgs,
        'acc':acc,
        'csvform':csvform,
        'services_category':Service_Category.objects.all(),
    }
    return render(request,"email_clients.html",context)


@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            msg = request.POST.get('mail')
            tag = request.POST.get('tag')
            customer_count = request.POST.get('customer_count')
            if ((int(customer_count))*0.5) > request.user.wallet:
                messages.error(request,f'Campaign Failed! Please maintain sufficient balance to continue. Estimated amont {(int(customer_count))*0.5} required.')
                messages.info(request,f'Available amount {request.user.wallet}')
                return redirect('/mail/clients')
            thread = threading.Thread(target=send_bulk_emails,args = (request.user,msg,tag,customer_count))
            thread.start()
            messages.success(request,'Email sending Started.')
        except:
            messages.error(request,'Someting went wrong. Please follow the documentation.')
    return redirect('/home/transactions')
    
    
@login_required
def delete(request,id):
    try:
        messages.success(request,'Message deleted successfully !')
        Messages.objects.filter(user=request.user).filter(id=id).delete()
    except:
        pass
    return redirect('/mail/clients')