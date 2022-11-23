from tkinter import PhotoImage
from django.shortcuts import render, redirect
from datetime import datetime
from webapp.models import Contact, Profile
from django.contrib import messages
from django.contrib.auth.models import User
from gfg import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_tokens
from django.core.mail import EmailMessage
from django.contrib.auth import login, authenticate, logout
import uuid
from .helpers import send_forget_password_mail
from .form import ImageForm
from .models import Image
from django.contrib.sessions.models import Session

# Create your views here.
def index(request):
    return render(request, "authentication/index.html") 
def dashboard(request):
    if request.session.has_key('uid'): 
        if request.method == "POST":
            form =  ImageForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()         
                obj = form.instance
                return render(request, "authentication/dashboard.html", {"obj": obj})
                # return render(request, "authentication/dashboard.html")
            else:
                messages.error(request, "fill form completely")    

        form = ImageForm()    
        img = Image.objects.all()
        
        template = "authentication/dashboard.html"
        directory = {"img":img, 
                    "form": form}
        return render(request, template , directory)
    else:
        return redirect('loginn')       
def about(request):
    return render(request, "authentication/about.html") 
def privacy(request):
    return render(request, "authentication/privacy.html") 
def terms(request):
    return render(request, "authentication/terms.html")
def contact(request):
    if request.method == "POST":
        name =  request.POST.get('name')
        email =  request.POST.get('email')
        phone =  request.POST.get('phone')
        desc =  request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Request Sent!')
        return redirect('contact')
    return render(request, "authentication/contact.html")       
# contact form tak hugya ab agay k saray functions GFG_5 se uthany hain
def loginn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('loginn')

        user = authenticate(username=username, password=password)
        if not user_obj.is_active:
            messages.error(request, "account not verified")    
            return redirect('loginn')
        
        else:
            if user is not None:
                login(request, user)
                request.session['uid'] = request.POST['username']
                return redirect('dashboard')
            else:
                messages.error(request, "bad credentials")    
                return redirect('loginn')
    return render(request, "authentication/login.html")
def register(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username=username):
            messages.error(request, "username already exists!")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, "email already registered!")
            return redirect('register')         
        if len(username) > 20:
            messages.error(request, "username must be under 20 characters")
            return redirect('register')
        if len(password) < 8:
           messages.error(request, "password must be atleast 8 characters")
           return redirect('register')      
        if password != password2:
            messages.error(request, "passwords didn't matched!") 
            return redirect('register')    
        if not username.isalnum():
            messages.error(request, "username must be alpha-numeric only")
            return redirect('register')

        user_obj = User(username = username, email = email)    
        user_obj.set_password(password)
        user_obj.first_name = fname
        user_obj.last_name = lname
        user_obj.is_active =False
        user_obj.save()

        profile_obj = Profile.objects.create(user = user_obj)
        profile_obj.save()

        # messages.success(request, "Account created. Please check your inbox, we have sent a confirmation email")

        # welcome email code

        subject = "Welcome to Spiritual Humanity"
        message = "Hello " + user_obj.first_name + "! \n" + "Welcome to our cummunity\n Thanks!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [user_obj.email]
        send_mail(subject, message, from_email, to_list, fail_silently= True)

        # email confirmation code

        current_site = get_current_site(request)
        email_subject = "Confirm your account on Spiritual Humanity"
        message2 = render_to_string('email_confirmation.html',{
            'name': user_obj.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
            'token': generate_tokens.make_token(user_obj)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user_obj.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('confirmation')   
    return render(request, "authentication/register.html") 
def signout(request):
    # request.session['uid'] = request.POST.get('username')
    # del request.session['uid']
    logout(request)
    # messages.success(request, "logged out")
    return redirect('loginn')     
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_tokens.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, 'Your account has been verified.')
        uid= None
        return redirect('loginn')
    else:
        return render(request, 'activation_failed.html')     
def forgot_pass(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.success(request, "username do not exist")
                return redirect('/forgot-password/')
                
            user_obj = User.objects.get(username = username)   
            token = str(uuid.uuid4()) 
            
            profile_obj = Profile.objects.get(user = user_obj)            
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            # messages.success(request, "email sent")
            # return redirect('/forgot-password/')
            return redirect('reset_email') 
            
    except Exception as e:
        print(e)        
    return render(request, "authentication/forget_pass.html")      
def change_pass(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        # print(profile_obj)
        context = {'user_id' : profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, "no user found")
                return redirect(f"/change-password/{token}/")

            if new_password != confirm_password:
                messages.success(request, "passwords didn't match!")
                return redirect(f"/change-password/{token}/")
            if len(new_password) < 8:
                messages.error(request, "password must be atleast 8 characters")
                return redirect(f"/change-password/{token}/")

            user_obj = User.objects.get(id = user_id)    
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, "password updated successfuly")
            return redirect('/login')


    except Exception as e:
        print(e)

    return render(request, "authentication/change_pass.html", context)          
def reset_email(request):
    return render(request, "authentication/reset_email.html")
def confirmation(request):
    return render(request, "authentication/confirmation.html")       
def radioexample(request):
   if request.method=="POST":
      cs = request.POST["course"]
      return render(request,"authentication/radioexample.html",{"res":cs})
   return render(request,"authentication/radioexample.html")
def radiodesign(request):
	return render(request,"authentication/radiodesign.html")
def radiocode(request):
	color = request.POST["color"]
	return render(request,"authentication/radiodesign.html",{'key':color})   
