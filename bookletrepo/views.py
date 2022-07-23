
from email.message import EmailMessage
import os
from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import path
from django.core.mail import EmailMessage
from myproject import settings
from .models import FilesAdmin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token



# Create your views here.
def home(request):
    context = {'file':FilesAdmin.objects.all()}
    return render(request, "bookletrepo/index.html", context)
def signup(request):
    if request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists! Please try other')
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request, 'Email already registered ! Please try other')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords does not match")
        if not username.isalnum():
            messages.error(request,"Username must be alpha-numeric only")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.is_active=False
        myuser.save()
        messages.success(request, "Your account has been created successfully ! Please check your email account to verify the login details")

        current_site = get_current_site(request)
        subject = "Confirm your email - Account Verification - Booklet Repository Login"
        message = render_to_string('email_confirmation.html',{
            'name': myuser.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
       
        email.send()


        return redirect('signin')
    return render(request, "bookletrepo/signup.html")
def signin(request):
    if request.method=="POST":
        username = request.POST['username']
        password1 = request.POST['password']

        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
        else:
            messages.error(request, "Invalid Username/Password")
            return redirect("home")
    return render(request, "bookletrepo/signin.html")
def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect("home")

def download(request, path):
    file_path=os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response=HttpResponse(fh.read(), content_type="application/adminupload")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response
    raise Http404

def activate(request, uidb64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')