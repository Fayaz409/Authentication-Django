from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,authenticate
# Create your views here.
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm


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