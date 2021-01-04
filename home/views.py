from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.http import request
from django.shortcuts import redirect, render


def index(request):
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'home/about.html')


def demo(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('accounts:dashboard')
    elif request.method == 'POST':
        if 'Manager' in request.POST:
            user = authenticate(username='Manager', password='DemoMgr123@#')
            auth.login(request, user)
            messages.success(
                request, f"You are now logged in as Project Manager")
            return redirect('accounts:dashboard')
        elif 'Developer' in request.POST:
            user = authenticate(username='Developer', password='DemoDvl123@#')
            auth.login(request, user)
            messages.success(
                request, f"You are now logged in as Developer")
            return redirect('accounts:dashboard')
        elif 'Admin' in request.POST:
            user = authenticate(username='Admin', password='Admin123@#')
            auth.login(request, user)
            messages.success(
                request, f"You are now logged in as Admin")
            return redirect('accounts:dashboard')
        elif 'EndUser' in request.POST:
            user = authenticate(username='EndUser', password='EUsr123@#')
            auth.login(request, user)
            messages.success(
                request, f"You are now logged in as the End User")
            return redirect('accounts:dashboard')
    return render(request, 'home/demo.html')


def handle404(request, exception):
    return render(request, template_name="404.html", status=404)


def handle403(request, exception):
    return render(request, template_name="403.html", status=403)
