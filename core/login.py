import requests
import os
from dotenv import load_dotenv
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

load_dotenv()

def cronos_admin_login(request):
    if request.method == 'POST':
        username: str = request.POST['username']
        password: str = request.POST['password']
        if username == "admin":
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('admin:index'))
            else:
                messages.error(request, 'Invalid Email or password.')
                return render(request, 'admin/login.html')

        response = requests.post(os.getenv("AUTH_CRONOS"), data={'emailrq': username, 'senharq': password})

        if response.status_code == 200:
            user = user = User.objects.filter(username=username).first()
            if user is not None:
                auth_user = authenticate(request, username=username, password=password)
                if auth_user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('admin:index'))
                else:
                    user.set_password(password)
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect(reverse('admin:index'))
            else:
                user = User.objects.create_user(username, password=password)
                user.is_staff = True
                user.email = username
                name = username.split("@")[0].split(".")
                user.first_name = name[0]

                if len(name) > 1:
                    user.last_name = name[1]

                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse('admin:index'))

        else:
            messages.error(request, 'Invalid Email or password.')
            return render(request, 'admin/login.html')
        
    else:
        return render(request, 'admin/login.html')