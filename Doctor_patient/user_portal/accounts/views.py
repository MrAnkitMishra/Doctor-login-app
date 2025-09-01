from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import Profile

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            Profile.objects.create(
                user=user,
                user_type=form.cleaned_data["user_type"],
                profile_picture=form.cleaned_data.get("profile_picture"),
                address_line1=form.cleaned_data["address_line1"],
                city=form.cleaned_data["city"],
                state=form.cleaned_data["state"],
                pincode=form.cleaned_data["pincode"],
            )
            messages.success(request, "Signup successful! Please login.")
            return redirect("login")
        else:
            messages.error(request, "Signup failed. Please check the form.")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            profile, created = Profile.objects.get_or_create(user=user)
            if profile.user_type == "Patient":
                return redirect("patient_dashboard")
            elif profile.user_type == "Doctor":
                return redirect("doctor_dashboard")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


@login_required
def patient_dashboard(request):
    return render(request, "patient_dashboard.html", {"profile": request.user.profile})


@login_required
def doctor_dashboard(request):
    return render(request, "doctor_dashboard.html", {"profile": request.user.profile})
