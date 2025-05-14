from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegisterForm
from members.models import Members


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            if User.objects.filter(email=email).exists():
                messages.warning(request, f'An account with {email} already exists. Login or change your password if you dont remembers.')
                return render(request, 'users/register.html', {'form':form})
            
            user = form.save(commit=False)
            if user.email.endswith('@church.com'):
                user.is_staff = True
            else:
                messages.warning(request, f'You do not have the rights to be a staff, contact the site admin.')
                return render(request, 'users/register.html', {'form':form})
            
            user.save()
            messages.success(request, f'Account for {user.username} created succefully.')
            return redirect('user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            if user.is_superuser:
                login(request, user)
                messages.success(request, f'Log in successfull')
                return redirect('/admin/')
            elif user.is_staff:
                login(request, user)
                messages.success(request, f'Log in successfull')
                return redirect('members_all')
            else:
                messages.error(request, f'You do not have access to this section. Log in with the appropriate page!')
                return redirect('user_login')
        else:
            return render(request, 'users/login.html', {'form':form, 'error':'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form':form})


def member_account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # user = form.save()
            unique_id = form.cleaned_data['username']
            try:
                member = Members.objects.get(unique_id=unique_id)
                if member.user:
                    return render(request, 'users/member_create_account.html', {'form':form, 'error':'This ID has already been used to create an accout.'})
                
                user = form.save(commit=False)
                user.email_address = member.email_address
                user.save()
                member.user = user
                member.save()
                # login(request, user)
                return redirect('member_login')
            except Members.DoesNotExist:
                return render(request, 'users/member_create_account.html', {'form':form, 'error':'Invalid Unique ID. Please use the ID sent to your email if you have been registered, if not kindly contact the church clerk.'})
    else:
        form = UserCreationForm()
    return render(request, 'users/member_create_account.html', {'form':form})

def member_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, 'members'):
                login(request, user)
                messages.success(request, f'Log in successfull')
                return redirect('individual_member', pk = user.members.pk)
            else:
                messages.error(request, 'Invalid credintials. Please use the appropriate login page!')
                return redirect('member_login')
            
        else:
            return render(request, 'users/member_login.html', {'form':form, 'error':'Invalid username or password!'})
            
    else:
        form = AuthenticationForm()
    return render(request, 'users/member_login.html', {'form':form})


