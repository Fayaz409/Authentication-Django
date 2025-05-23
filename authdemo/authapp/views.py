from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from django.contrib.auth.forms import UserChangeForm,AuthenticationForm,PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash,logout,login,authenticate
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import EditEmployeeForm,SignUpForm,ProfileChangeForm,RoleForm,CreateStaffEmployeeForm


@login_required
def index(request):
    return render(request,'authapp/index.html')

def signup(request):
    form = SignUpForm()
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add user to Customers Group
            customers_group,created = Group.objects.get_or_create(name='Customers')
            user.groups.add(customers_group)

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

@login_required
def delete_account(request):
    if request.method=='POST':
        request.user.delete()
        return redirect('login')
    return render(request,'authapp/delete_account.html')

@login_required
def signout(request):
    logout(request)
    return redirect('login')

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def roles_list(request):
    roles = Group.objects.all()
    return render(request,'authapp/roles_list.html',{'roles':roles})

@login_required
@user_passes_test(is_superuser)
def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles-list')
    else:
        form = RoleForm()
    return render(request,'authapp/create_role.html',{'form':form})

@login_required
@user_passes_test(is_superuser)
def edit_role(request,name):
    role_name = Group.objects.get(name=name)
    if request.method == 'POST':
        form = RoleForm(request.POST,instance=role_name)
        if form.is_valid():
            form.save()
            return redirect('roles-list')
    else:
        form = RoleForm(instance=role_name)
    return render(request,'authapp/update_role.html',{'form':form})

@login_required
@user_passes_test(is_superuser)
def delete_role(request,role_id):
    role = Group.objects.get(id=role_id)

    if request.method == 'POST':
        groupUsers = Group.objects.filter(id=role_id).count()
        if(groupUsers == 0):
            role.delete()
            return redirect('roles-list')
        else:
            return HttpResponse('This Role is Not Empty. So, It Can Not be Deleted')

    return render(request,'authapp/delete_role.html',{'role':role})

@login_required
@user_passes_test(is_superuser)
def staff_list(request):
    staff_members = User.objects.filter(is_staff=True)
    return render(request,'authapp/staff_list.html',{'staff_members':staff_members})

@login_required
@user_passes_test(is_superuser)
def create_staff_employee(request):
    if request.method == 'POST':
        form  = CreateStaffEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            role_name = form.cleaned_data.get('role')
            staff_group,created = Group.objects.get_or_create(name=role_name)
            user.groups.add(staff_group)
            return redirect('staff-list')
    else:
        form = CreateStaffEmployeeForm()
    return render(request,'authapp/create_staff_employee.html',{'form':form})

@login_required
@user_passes_test(is_superuser)
def edit_staff_employee(request,user_id):
    staff_member = get_object_or_404(User, pk=user_id)
    # Safely grab the first group, or None
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST,instance=staff_member)
        if form.is_valid():
            user = form.save()
            role_name = form.cleaned_data.get('role')
            staff_group,created = Group.objects.get_or_create(name = role_name)
            user.groups.clear()
            user.groups.add(staff_group)
            return redirect('staff-list')
    else:
        staff_group = staff_member.groups.first()

        # Optionally: handle no-group scenario
        if staff_group is None:
            messages.warning(request, "This user has no staff group assigned.")
            # e.g. assign a default group, or redirect back
            # return redirect('staff-list')

        form = EditEmployeeForm(instance=staff_member)

    return render(request,'authapp/edit_staff_employee.html',{'form':form,'staff_member':staff_member,'staff_group':staff_group,'staff_group_id': staff_group.id if staff_group else None})