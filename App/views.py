from django.shortcuts import render ,redirect, HttpResponseRedirect
from .form import *
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from BlogPress.decorators import get_ip

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
            # post = form.save(commit=False)
            # post.save()

            # Profile(user=post).save()

            username = form.cleaned_data.get("username")
            email    = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user     = authenticate(username=username, password=raw_password)

            msg      = 'User created.'
            success  = True

            messages.success(request, 'Registration Completed Successfully. Kindly Login to Continue.')
            return HttpResponseRedirect("/login/")

        else:
            print(form.errors)  
    else:
        form = SignUpForm()
    return render(request ,'register.html' ,{"form": form, "msg" : msg, "success" : success })

def policy(request):
    return render(request ,'policy.html')

def blog_detail(request ,slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug = slug).first()
        context['blog_obj'] =  blog_obj
    except Exception as e:
        print(e)
    return render(request ,'blog_detail.html' ,context)

def see_blog(request):

    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user = request.user)
        context['blog_objs'] =  blog_objs
    
    except Exception as e: 
        print(e)
    
    print(context)
    return render(request ,'see_blog.html' ,context)


def add_blog(request):
    context = {'form' : BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user
            
            if form.is_valid():
                content = form.cleaned_data['content']
            
            blog_obj = BlogModel.objects.create(
                user = user , title = title, 
                content = content, image = image
            )
            print(blog_obj)
            return redirect('/add-blog/')

    except Exception as e :
        print(e)
    
    return render(request ,'add_blog.html' ,context)


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

def blog_delete(request ,id):
    try:
        blog_obj = BlogModel.objects.get(id = id)
        
        if blog_obj.user == request.user:
            blog_obj.delete()
        
    except Exception as e :
        print(e)

    return redirect('/see-blog/')

def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token = token).first()
        
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e : 
        print(e)
    
    return redirect('/')