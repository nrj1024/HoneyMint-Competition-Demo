from django.shortcuts import render
from contestpage.models import Contestant
from django.views.defaults import page_not_found
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

def home(request):
    return render(request,'HoneyMint.html')

def register(request, user_id=None):
    if user_id!=None:
        c=Contestant.objects.all()
        arr=[]
        for i in c:
            arr.append(i.id)
        if user_id not in arr:
            return page_not_found(request,'Page Not Found!')
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone=request.POST['phone']
        email=request.POST['email']

        c=Contestant.objects.all()
        arr=[]
        for i in c:
            arr.append(i.email)
            arr.append(i.phone)
        if phone in arr or email in arr:
            return render(request, 'PromoRegister.html',{'same':True})
        cur=Contestant.objects.create(first_name=first_name,last_name=last_name,phone=phone,email=email,entries=1)
        
        subject = 'Welcome to the HoneyMint contest!'
        html_message = render_to_string('Mail.html', {'id': cur.id})
        plain_message = strip_tags(html_message)
        from_email = 'HoneyMint@mail.com'
        to = cur.email

        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        if user_id!=None:
            inv=Contestant.objects.get(id=user_id)
            inv.entries=inv.entries+1
            inv.save()
        return render(request, 'PromoRegister.html',{'success':True})
    return render(request,'PromoRegister.html', {'success':False})
    
def checkin(request):
    if request.method=='POST':
        creds=request.POST['email']
        contestant=Contestant.objects.filter(email=creds).first()
        if contestant==None:
            return render(request, 'Checkin.html', {'notfound':True})
        else:
            return render(request, 'Status.html', {'name':contestant.first_name, 'entries':contestant.entries})
    return render(request, 'Checkin.html')

def leaderboard(request):
    contestants=[]
    for i in Contestant.objects.all():
        contestants.append(i)
    contestants.sort(key=lambda x:x.entries,reverse=True)
    rank=0
    fmt_contestants=[]
    for contestant in contestants:
        hashmap={}
        hashmap['rank']=rank=rank+1
        hashmap['name']=contestant.first_name+' '+contestant.last_name
        hashmap['email']=contestant.email
        hashmap['entries']=contestant.entries
        fmt_contestants.append(hashmap)

    return render(request,'Leaderboard.html',{'contestants':fmt_contestants})