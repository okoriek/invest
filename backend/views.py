from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from . models import *
from . form import *
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from . utils import *
from django.core.mail import EmailMessage

def home(request):
    return render(request, 'backend/index.html')


def EmailVerification(request, uidb64, token):
    try:
        uid =  force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError,ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and TokenGenerator.check_token(user, token):
        user.is_active=  True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Email verification complete' )
    return redirect('/login')


def register(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active =False
            user.save()
            website = get_current_site(request).domain
            email_subject = 'Email Verification'
            email_body =  render_to_string('email/activation.html',{
                'user':user.first_name,
                'domain':website,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': TokenGenerator.make_token(user)
            })
            email = EmailMessage(subject=email_subject, body=email_body,
                from_email='Quantumaiwealth <test@saxsvualts.com>', to=[user.email]
                )
            email.content_subtype = 'html'
            email.send()
            messages.success(request, f"We've sent a verification email. Please check your inbox or spam folder to activate your account")
            return redirect('/login')
    else:    
        form = RegistrationForm()
    args = {'form':form}
    return render(request, 'backend/register.html', args)


def login_user(request):
    if request.method == 'POST':
        email =  request.POST.get('email')
        password = request.POST.get('password')
        
        active =  User.objects.get(email=email)
        if active.is_active == True:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                next_url = request.POST.get('next', request.GET.get('next'))
        
                if next_url:
                    return redirect(next_url)
                else:
                    print('loging')
                    return redirect(reverse('backend:dashboard'))            
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Your account is currently inactive, Please contact support for assistance.')
            return redirect(reverse('backend:login'))
    return render(request, 'backend/login.html')


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
