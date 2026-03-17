from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.utils.timezone import now

from .models import Job, JobApplication
from accounts.models import Application

from .models import JobApplication


from django.http import HttpResponse


# ❌ OLD direct imports (kept but disabled safely)
# from reportlab.lib.colors import HexColor, white, black
# from reportlab.lib.utils import ImageReader


from django.conf import settings
import os


# ❌ OLD duplicate try block (kept but disabled safely)
# try:
#     from reportlab.pdfgen import canvas
# except ImportError:
#     canvas = None


# ================== FINAL SAFE IMPORT ==================
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.utils import ImageReader

except ImportError:
    canvas = None
    A4 = None # type: ignore
    inch = None # type: ignore
    HexColor = None
    white = None
    black = None
    ImageReader = None
# ======================================================



# Create your views here.


@login_required
def recruiter_dashboard_analytics(request):
    recruiter = request.user.recruiterprofile
    today = now().date()

    jobs = Job.objects.filter(recruiter=recruiter).annotate(
        applicant_count=Count("applications")
    )

    total_jobs = jobs.count()
    active_jobs = jobs.filter(deadline__gte=today).count()
    closed_jobs = jobs.filter(deadline__lt=today).count()
    total_applicants = Application.objects.filter(
        job__recruiter=recruiter
    ).count()

    chart_labels = []
    chart_data = []

    for job in jobs.order_by("id"):
        chart_labels.append(job.job_title)
        chart_data.append(job.applicant_count) # type: ignore

    context = {
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "closed_jobs": closed_jobs,
        "total_applicants": total_applicants,
        "chart_labels": chart_labels,
        "chart_data": chart_data,
    }
    return render(request, "jobs/recruiter_analytics.html", context)


@login_required
def job_applicant_list(request, job_id):
    recruiter = request.user.recruiterprofile
    job = get_object_or_404(Job, id=job_id, recruiter=recruiter)

    applicants = Application.objects.filter(job=job).select_related("applicant")

    context = {
        "job": job,
        "applicants": applicants,
    }
    return render(request, "jobs/job_applicant_list.html", context)


@login_required
def job_search_suggestions(request):
    query = request.GET.get("q", "").strip()
    recruiter = request.user.recruiterprofile

    suggestions = []

    if query:
        jobs = Job.objects.filter(
            recruiter=recruiter,
            job_title__icontains=query
        ).order_by("job_title")[:8]

        suggestions = list(jobs.values_list("job_title", flat=True))

    return JsonResponse({"results": suggestions})


@login_required
def create_new_jobs(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        company_logo = request.FILES.get('company_logo')
        responsibilities = request.POST.get('responsibilities')
        education = request.POST.get('education')
        vacancies = request.POST.get('vacancies')
        salary = request.POST.get('salary')
        currency = request.POST.get('currency')
        job_type = request.POST.get('job_type')
        description = request.POST.get('description')
        skills = request.POST.get('skills')
        opening_date = request.POST.get('opening_date')
        deadline = request.POST.get('deadline')
        location = request.POST.get('location')

        recruiter = request.user.recruiterprofile

        Job.objects.create(
            recruiter=recruiter,
            job_title=job_title,
            company_name=company_name,
            company_logo=company_logo,
            responsibilities=responsibilities,
            education=education,
            vacancies=vacancies,
            salary=salary,
            currency=currency,
            job_type=job_type,
            description=description,
            skills=skills,
            opening_date=opening_date,
            deadline=deadline,
            location=location
        )

        messages.success(request, 'Job created successfully!')
        return redirect('profile')

    return render(request, 'jobs/create_new_jobs.html')


@login_required
def view_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    applications_count = Application.objects.filter(job=job).count()

    context = {
        "job": job,
        "applications_count": applications_count
    }

    return render(request, "jobs/view_job.html", context)


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        job.job_title = request.POST.get('job_title')
        job.company_name = request.POST.get('company_name')
        job.vacancies = request.POST.get('vacancies')
        job.salary = request.POST.get('salary')
        job.currency = request.POST.get('currency')
        job.job_type = request.POST.get('job_type')
        job.opening_date = request.POST.get('opening_date')
        job.deadline = request.POST.get('deadline')
        job.location = request.POST.get('location')
        job.education = request.POST.get('education')
        job.responsibilities = request.POST.get('responsibilities')
        job.skills = request.POST.get('skills')
        job.description = request.POST.get('description')

        if request.FILES.get('company_logo'):
            job.company_logo = request.FILES.get('company_logo')

        job.save()

        messages.success(request, "Job updated successfully")
        return redirect('recruiter_analytics')

    context = {
        'job': job
    }

    return render(request, 'jobs/edit_job.html', context)


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully")
        return redirect('recruiter_analytics')

    context = {
        'job': job
    }

    return render(request, 'jobs/delete_job.html', context)



# def download_job_pdf(request, job_id):
#     job = get_object_or_404(Job, id=job_id)
#     (ALL YOUR COMMENTED CODE REMAINS SAME — untouched)



def download_job_pdf(request, job_id):

    if canvas is None:
        return HttpResponse("PDF feature is not available on this server.", status=503)

    job = get_object_or_404(Job, id=job_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{job.job_title}.pdf"'

    p = canvas.Canvas(response, pagesize=A4) # type: ignore

    width, height = A4 # type: ignore
    y = height - 60

    p.setFont("Helvetica-Bold", 22)
    p.drawString(60, y, job.job_title)

    p.setFont("Helvetica", 14)
    y -= 25
    p.drawString(60, y, job.company_name)

    if job.recruiter.company_website:
        y -= 18
        p.drawString(60, y, job.recruiter.company_website)

    status = "Open" if not job.is_closed else "Closed"

    p.setFont("Helvetica-Bold", 12)
    p.drawRightString(width-60, height-60, status)

    if job.company_logo:

        logo_path = os.path.join(settings.MEDIA_ROOT, job.company_logo.name)

        if os.path.exists(logo_path):

            logo = ImageReader(logo_path) # type: ignore

            p.drawImage(
                logo,
                width-160,
                height-130,
                width=80,
                height=80,
                preserveAspectRatio=True
            )

    y -= 40

    p.setFont("Helvetica-Bold", 11)

    p.drawString(60, y, "Vacancies:")
    p.drawString(200, y, "Salary:")
    p.drawString(350, y, "Location:")

    y -= 18

    p.setFont("Helvetica", 11)

    p.drawString(60, y, str(job.vacancies))
    p.drawString(200, y, f"{job.salary} {job.currency}")
    p.drawString(350, y, job.location)

    y -= 30

    p.setFont("Helvetica-Bold", 11)

    p.drawString(60, y, "Opening Date:")
    p.drawString(230, y, "Deadline:")
    p.drawString(380, y, "Applications:")

    y -= 18

    p.setFont("Helvetica", 11)

    p.drawString(60, y, job.opening_date.strftime("%d %B %Y"))
    p.drawString(230, y, job.deadline.strftime("%d %B %Y"))
    p.drawString(380, y, str(job.applications.count())) # type: ignore

    y -= 30

    def draw_section(title, text):

        nonlocal y

        p.setFont("Helvetica-Bold", 14)
        p.drawString(60, y, title)

        y -= 20

        p.setFont("Helvetica", 11)

        lines = text.split("\n")

        for line in lines:

            if y < 80:
                p.showPage()
                y = height - 60

            p.drawString(70, y, line.strip())
            y -= 16

        y -= 10

    draw_section("Education", job.education)
    draw_section("Skills", job.skills)
    draw_section("Responsibilities", job.responsibilities)
    draw_section("Description", job.description)

    p.save()

    return response





def job_detail(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    has_applied = False

    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(
            job=job,
            applicant=request.user
        ).exists()

    context = {
        'job': job,
        'has_applied': has_applied
    }

    return render(request, 'jobs/job_detail.html', context)