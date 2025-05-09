from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserChangeForm,AuthenticationForm,PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash,login,authenticate
# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,ProfileChangeForm


@login_required
def index(request):
    return render(request,'authapp/index.html')

def signup(request):
    form = SignUpForm()
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    return render(request,'authapp/signup.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
            return redirect('home')
    else:
      form = AuthenticationForm()
    return render(request,'authapp/login.html',{'form':form}) 

@login_required
def change_pasword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'authapp/change_password.html',{'form':form})

@login_required
def change_profile(request):
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileChangeForm(instance=request.user)
    return render(request,'authapp/change_profile.html',{'form':form})