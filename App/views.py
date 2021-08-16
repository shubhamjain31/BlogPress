from django.shortcuts import render ,redirect, HttpResponseRedirect
from .form import *
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from BlogPress.decorators import *
from validators import is_invalid

from cryptography.fernet import Fernet
from cryptography import *
import cryptography
from django.core.mail import EmailMessage

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('/')

def home(request):
    context = {'blogs' : BlogModel.objects.all()}
    return render(request ,'home.html' ,context)

def login_view(request):
    return render(request ,'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)

        agree = request.POST.get("agree")
        if agree is None:
            msg = 'Please Acccept Privacy Policy'
            return render(request, "register.html", {"form": form, "msg" : msg, "success" : success })

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            Profile(user=post).save()

            username        = form.cleaned_data.get("username")
            email           = form.cleaned_data.get("email")
            raw_password    = form.cleaned_data.get("password1")

            token  = encryption_key(post.pk)
            user   = User.objects.get(email=email)

            user     = authenticate(username=username, password=raw_password)

            msg      = 'User created.'
            success  = True

            subject  = 'BlogPress Email Verification'

            body     = '<h1>Welcome!</h1>,<br><br>\
                Thanks for signing up! We just need you to verify your email address to complete setting up your account.<br>\
                <a href="http://127.0.0.1:8000/verification/' + str(token.decode())+'"><button>Verify My Email</button></a><br><br>\
                For any questions, you can write to us at demo@gmail.com.<br><br> \
                Thanks & Regards,<br>\
                Team BlogPress<br>\
                demo@gmail.com<br>'

            msg = EmailMessage(subject, body, 'BlogPress', to=[email])
            msg.content_subtype = "html"
            msg.send()

            email_verification(user=user, verification_link=token.decode(), ip_address=get_ip(request)).save()

            messages.success(request, 'Registration Completed Successfully. Please Check Your Email.!')
            return HttpResponseRedirect("/login/")

        else:
            print(form.errors)  
    else:
        form = SignUpForm()
    return render(request ,'register.html' ,{"form": form, "msg" : msg, "success" : success })

def policy(request):
    return render(request ,'policy.html')

def verification(request, val):
    pk_ = decryption_key(val)

    try:
        user_obj = Profile.objects.get(user=int(pk_))

        user_obj.is_verified = True
        user_obj.save()
        return redirect('/')

    except Exception as e : 
        print(e)

    return redirect('/')

@login_required(login_url="/login/")
def blog_detail(request ,slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug = slug).first()
        context['blog_obj'] =  blog_obj
    except Exception as e:
        print(e)
    return render(request ,'blog_detail.html' ,context)

@login_required(login_url="/login/")
def see_blog(request):

    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user = request.user)
        context['blog_objs'] =  blog_objs
    
    except Exception as e: 
        print(e)
    
    print(context)
    return render(request ,'see_blog.html' ,context)

@login_required(login_url="/login/")
def add_blog(request):
    context = {'form' : BlogForm}
    try:
        if request.method == 'POST':
            form    = BlogForm(request.POST)
            
            image   = request.FILES.get('image','')
            title   = request.POST.get('title')
            user    = request.user
            
            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user = user , title = title, 
                content = content, image = image,
                ip_address = get_ip(request), browser = get_browser(request)
            )
            return redirect('/add-blog/')

    except Exception as e :
        print(e,'jddj')
    
    return render(request ,'add_blog.html' ,context)

@login_required(login_url="/login/")
def blog_update(request ,slug):
    context = {}
    try: 
        blog_obj = BlogModel.objects.get(slug = slug)
       
        if blog_obj.user != request.user:
            return redirect('/')
        
        initial_dict = {'content': blog_obj.content}

        form = BlogForm(initial = initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            
            image       = request.FILES['image']
            title       = request.POST.get('title')

            user = request.user
            
            if form.is_valid():
                content = form.cleaned_data['content']
            
            blog_obj = BlogModel.objects.create(
                user = user , title = title, 
                content = content, image = image
            )
        
        context['blog_obj']     = blog_obj
        context['form']         = form
    except Exception as e :
        print(e)

    return render(request ,'update_blog.html' ,context)

@login_required(login_url="/login/")
def blog_delete(request ,id):
    try:
        blog_obj = BlogModel.objects.get(id = id)
        
        if blog_obj.user == request.user:
            blog_obj.delete()
        
    except Exception as e :
        print(e)

    return redirect('/see-blog/')

@login_required(login_url="/login/")
def profile(request, name):
    return render(request ,'profile.html' )

@login_required(login_url="/login/")
def settings(request):
    last = request.META.get('HTTP_REFERER', None)

    if request.method == 'POST':
        firstname       = request.POST.get('firstname')
        lastname        = request.POST.get('lastname')
        email           = request.POST.get('email')
        mobile          = request.POST.get('mobile')
        about           = request.POST.get('about')
        profile_image   = request.FILES.get('profile_image', '')

        if str(profile_image).endswith('.png'):
            messages.error(request, "Please Upload Logo in .jpg or .jpeg Format")
            return HttpResponseRedirect(last)

        if firstname == "" or is_invalid(firstname):
            messages.error(request, "Please Enter First Name")
            return HttpResponseRedirect(last)

        if lastname == "" or is_invalid(lastname):
            messages.error(request, "Please Enter Last Name")
            return HttpResponseRedirect(last)

        if email == "" or is_invalid(email):
            messages.error(request, "Please Enter an Email")
            return HttpResponseRedirect(last)

        if mobile == "" or is_invalid(mobile):
            messages.error(request, "Please Enter a Mobile Number")
            return HttpResponseRedirect(last)

        if about == "" or is_invalid(about):
            messages.error(request, "Please Write Something In Your Bio")
            return HttpResponseRedirect(last)

        user_obj = User.objects.get(pk=request.user.id)
        user_obj.first_name     = firstname.capitalize()
        user_obj.last_name      = lastname.capitalize()
        user_obj.email          = email
        user_obj.save()

        user_profile = Profile.objects.get(user = user_obj)
        user_profile.image      = profile_image
        user_profile.mobile     = mobile
        user_profile.about      = about.capitalize()
        user_profile.ip_address = get_ip(request)
        user_profile.save()

        messages.success(request, 'Profile Information Added Successfully!')
        return HttpResponseRedirect(last)

    user_obj        = User.objects.get(pk=request.user.id)
    user_profile    = Profile.objects.get(user = user_obj)

    params = {'user_obj':user_obj, 'user_profile':user_profile}

    return render(request ,'settings.html' ,params)