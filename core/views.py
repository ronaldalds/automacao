import requests
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login


def cronos_admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        username = str(username)
        password = str(password)
        next_url = request.GET.get('next', reverse('admin:index'))
        if username == "admin":
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next_url)
            else:
                messages.error(request, 'Invalid Email or password.')
                return render(request, 'admin/login.html')

        response = requests.post(
            "https://api.cronos.online.psi.br/api/auth",
            data={
                'emailrq': username,
                'senharq': password
            }
        )

        if response.status_code == 200:
            grupo_cronos = requests.post(
                "https://api.cronos.online.psi.br/api/token",
                data={
                    'token': response.json().get("Token")
                }
            )

            new_group, _ = Group.objects.get_or_create(
                name=grupo_cronos.json().get("grupo")
            )

            user = user = User.objects.filter(username=username).first()
            if user is not None:
                auth_user = authenticate(
                    request,
                    username=username,
                    password=password
                )

                if auth_user is not None:
                    new_group.user_set.add(user)
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect(next_url)
                else:
                    user.set_password(password)
                    new_group.user_set.add(user)
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect(next_url)
            else:
                user = User.objects.create_user(username, password=password)
                user.is_staff = True
                new_group.user_set.add(user)
                user.email = username
                name = username.split("@")[0].split(".")
                user.first_name = name[0]

                if len(name) > 1:
                    user.last_name = name[1]

                user.save()
                login(request, user)
                return HttpResponseRedirect(next_url)

        else:
            messages.error(request, 'Invalid Email or password.')
            return render(request, 'admin/login.html')

    else:
        return render(request, 'admin/login.html')
