from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.utils.timezone import now
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import Job
from accounts.models import Application


from django.http import HttpResponse
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor


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
        chart_data.append(job.applicant_count)

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


def download_job_pdf(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{job.job_title}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    width, height = A4
    y = height - 60

    blue = HexColor("#2563eb")

    # HEADER
    p.setFillColor(blue)
    p.rect(0, height - 120, width, 120, fill=1)

    p.setFillColor("white")
    p.setFont("Helvetica-Bold", 22)
    p.drawString(50, height - 70, job.job_title)

    p.setFont("Helvetica", 14)
    p.drawString(50, height - 95, job.company_name)

    y = height - 150

    p.setFillColor("black")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Vacancies:")
    p.drawString(200, y, "Salary:")
    p.drawString(350, y, "Location:")

    y -= 20

    p.setFont("Helvetica", 11)
    p.drawString(50, y, str(job.vacancies))
    p.drawString(200, y, f"{job.salary} {job.currency}")
    p.drawString(350, y, job.location)

    y -= 40

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Opening Date:")
    p.drawString(250, y, "Deadline:")

    y -= 20

    p.setFont("Helvetica", 11)
    p.drawString(50, y, job.opening_date.strftime("%d %B %Y"))
    p.drawString(250, y, job.deadline.strftime("%d %B %Y"))

    y -= 40

    def draw_section(title, text):

        nonlocal y

        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, title)

        y -= 20

        p.setFont("Helvetica", 11)

        lines = text.split("\n")

        for line in lines:

            if y < 80:
                p.showPage()
                y = height - 60

            p.drawString(60, y, line.strip())
            y -= 16

        y -= 10

    draw_section("Education", job.education)
    draw_section("Skills", job.skills)
    draw_section("Responsibilities", job.responsibilities)
    draw_section("Description", job.description)

    p.save()

    return response