from math import e
from multiprocessing import context
import re

from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib.auth import update_session_auth_hash

import jobs
from jobs.models import Job
from .models import CustomUser, RecruiterProfile, JobSeekerProfile




# Create your views here.
def home(request):

    jobs = Job.objects.all()

    context = {
        "jobs": jobs,
    }


    return render(request, 'accounts/index.html' , context)


# Registration logic here
def register(request):

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('home')
    

    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        profile_pic = request.FILES.get('profile_pic')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if not re.match(pattern, password):
            messages.error(request, "Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character.")
            return redirect('register')
        if CustomUser.objects.filter(username = user_name).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        
        if CustomUser.objects.filter(email = email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')
        
        if CustomUser.objects.filter(phone = phone).exists():
            messages.error(request, "Phone number already exists.")
            return redirect('register')
        
        user = CustomUser.objects.create_user(
            first_name = fname,
            last_name = lname,
            username = user_name,
            email = email,
            phone = phone,
            profile_pic = profile_pic,
            role = role,
            password = password
        )
        
        user.save()

        if role == 'recruiter':
            RecruiterProfile.objects.create(user = user)

        elif role == 'job_seeker':
            JobSeekerProfile.objects.create(user = user)


        messages.success(request, "✅ Registration successful. You can now login.")
        return redirect('login')
    

    return render(request, 'accounts/register.html')



# Login logic here
def login_view(request):

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('profile')

    if request.method == 'POST':

        # এখানে form থেকে username / email / phone যেটা user লিখবে সেটা নেওয়া হচ্ছে
        user_input = request.POST.get('user_name_email_phone')

        # এখানে password নেওয়া হচ্ছে
        password = request.POST.get('password')

        try:

            # এখানে database এ user খোঁজা হচ্ছে
            user_obj = CustomUser.objects.get(

                Q(username=user_input) |   # এখানে USERNAME check করবে

                Q(email=user_input) |      # এখানে EMAIL check করবে

                Q(phone=user_input)        # এখানে PHONE NUMBER check করবে

            )

            # এখানে authenticate করা হচ্ছে (login verify)
            user = authenticate(
                request,
                username=user_obj.username,  # authenticate সবসময় username দিয়ে হয়
                password=password
            )

            if user is not None:

                # login সফল হলে user session start হবে
                login(request, user)

                # success message
                messages.success(request, "Login Successful")

                # login হলে profile page এ redirect
                return redirect('profile')

            else:

                # password ভুল হলে এই message
                messages.error(request, "Invalid password")

        except CustomUser.DoesNotExist:

            # username / email / phone কোনটাই না মিললে এই message
            messages.error(request, "User not found")

    # GET request হলে login page show করবে
    return render(request, 'accounts/login.html')





def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


# @login_required
# def profile(request):

#     query = request.GET.get("q")

#     if request.user.role == "recruiter":
#         jobs = Job.objects.filter(recruiter=request.user.recruiterprofile)
    
#     elif request.user.role == "job_seeker":
#         jobs = Job.objects.none()

#     if query:
#         jobs = jobs.filter(job_title__icontains=query)

#     context = {
#         "jobs": jobs,
#         "today": now().date()
#     }

#     return render(request, 'accounts/profile.html', context)





@login_required
def profile(request):

    if request.user.role == "recruiter":

        recruiter_profile, created = RecruiterProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "job_title": "Senior HR Manager",
                "location": "Dhaka, Bangladesh",
                "company_name": "ONTAR IT",
                "company_overview": "Tech Solutions Ltd. is a fast-growing software company specializing in enterprise systems, mobile apps, and cloud services."
            }
        )

        jobs = Job.objects.filter(recruiter=recruiter_profile).order_by("id")

        q = request.GET.get("q", "").strip()

        if q:
            jobs = jobs.filter(job_title__icontains=q)

        context = {
            "jobs": jobs,
            "today": now().date(),
        }

        return render(request, "accounts/profile.html", context)

    else:

        profile, created = JobSeekerProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "title": "Frontend Developer",
                "location": "Dhaka, Bangladesh",
                "summary": "Passionate frontend developer with strong knowledge of HTML, CSS, Tailwind, JavaScript, and React. Looking for opportunities to build modern web apps.",
                "skills": "HTML CSS Tailwind JavaScript React",
                "experience": "Junior Web Developer — ABC Tech\n2024 - Present\nWorked on responsive UI, landing pages, and dashboard interfaces.",
                "email": request.user.email if request.user.email else "john@example.com",
                "phone": request.user.phone if request.user.phone else "+880 1234-567890",
                "linkedin": "https://linkedin.com/in/officialontar"
            }
        )

        updated = False

        if not profile.email and request.user.email:
            profile.email = request.user.email
            updated = True

        if not profile.phone and request.user.phone:
            profile.phone = request.user.phone
            updated = True

        if updated:
            profile.save()

        context = {
            "profile": profile,
        }

        return render(request, "accounts/profile.html", context)








@login_required
def edit_recruiter_profile(request):

    user = request.user
    recruiter = request.user.recruiterprofile

    if request.method == "POST":

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        recruiter.job_title = request.POST.get("job_title")
        recruiter.location = request.POST.get("location")
        recruiter.company_name = request.POST.get("company_name")
        recruiter.company_website = request.POST.get("company_website")
        recruiter.company_overview = request.POST.get("company_overview")


        # PROFILE IMAGE
        if request.FILES.get("profile_pic"):
            user.profile_pic = request.FILES.get("profile_pic")

        user.save()
        recruiter.save()

        messages.success(request, "Profile updated successfully")
        return redirect("profile")

    return render(request, "accounts/edit_recruiter_profile.html")





@login_required
def change_password(request):

    if request.method == "POST":

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        # Old password check
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect("change_password")

        # New password match
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect("change_password")

        # Old and new same check
        if old_password == new_password:
            messages.error(request, "New password cannot be same as old password.")
            return redirect("change_password")

        # Password change
        user.set_password(new_password)
        user.save()

        # Important: keep user logged in
        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully.")

        return redirect("change_password")

    return render(request, "accounts/change_password.html")