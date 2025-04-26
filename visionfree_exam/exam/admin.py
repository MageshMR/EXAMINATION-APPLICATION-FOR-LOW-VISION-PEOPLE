from django.contrib import admin
from .models import Answer

admin.site.register(Answer)


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def admin_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Ensure only admins can log in
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid credentials or not an admin user.")
    return render(request, "admin/login.html")

@login_required
def admin_dashboard(request):
    return render(request, "admin/dashboard.html")

def admin_logout(request):
    logout(request)
    return redirect("admin_login")



