from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
#register an account
def register(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    #not login
    else:
        if request.method == "POST":
            form=RegistrationForm(request.POST or None)

            if form.is_valid():
                user = None
                email = request.POST.get('email')
                if User.objects.filter(email = email).exists():
                    messages.warning(request,'Email đã tồn tại.')
                    return redirect('accounts:register')
                else:
                    user = form.save()
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=user.username,password=raw_password)
                    login(request,user)
                    return redirect("main:home")
        else:
            form=RegistrationForm()

        return render(request,'accounts/register.html', {"form": form})

#login
def login_user(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            #check user
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('main:home')
                else:
                    return render(request,'accounts/login.html',{"error": "Tài khoản của bạn chưa được kích hoạt."})
            else:
                return render(request,'accounts/login.html',{"error": "Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại."})

        return render(request,'accounts/login.html')
        
#Logout
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('accounts:login')
    else:
        return redirect('accounts:login')
    
def detail_user(request, id):
    detailuser = User.objects.get(id=id) #select * from Product where id=id
    context = {
        "detailuser": detailuser,
    }
    return render(request,'accounts/detail_user.html',context)

def edit_user(request, id):
    if request.user.is_authenticated:
        edituser = User.objects.get(id=id)
        edituser1 = Profile.objects.get(id=id)
        if request.method=='POST':
            form= UserForm(request.POST or None, instance=edituser)
            p_form=ProfileUpdateForm(request.POST, request.FILES or None, instance=edituser1)
            if form.is_valid() and p_form.is_valid():
                data1=form.save(commit=False)
                data2=p_form.save(commit=False)
                data1.save()
                data2.save()
                return redirect("accounts:detailuser",id)
        else:
            form= UserForm(instance=edituser)
            p_form= ProfileUpdateForm(instance=edituser1)
        return render(request,'accounts/adduser.html',{"form": form, "p_form": p_form, "controller": "Chỉnh Sửa Thông Tin"})
       #if not login
    return redirect('accounts:login')

