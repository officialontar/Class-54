from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.utils.timezone import now

from .models import Job
from accounts.models import Application


from django.http import HttpResponse
from reportlab.lib.colors import HexColor, white, black



from reportlab.lib.utils import ImageReader
from django.conf import settings
import os


try:
    from reportlab.pdfgen import canvas
except ImportError:
    canvas = None



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

#     response = HttpResponse(content_type="application/pdf")
#     response["Content-Disposition"] = f'attachment; filename="{job.job_title}.pdf"'

#     p = canvas.Canvas(response, pagesize=A4)
#     width, height = A4

#     blue = HexColor("#2563eb")
#     green = HexColor("#22c55e")
#     red = HexColor("#ef4444")
#     light_gray = HexColor("#f9fafb")
#     border_gray = HexColor("#e5e7eb")
#     text_gray = HexColor("#6b7280")
#     gold = HexColor("#facc15")

#     def draw_rounded_box(x, y, w, h, fill_color=light_gray, stroke_color=border_gray, radius=12):
#         p.setFillColor(fill_color)
#         p.setStrokeColor(stroke_color)
#         p.roundRect(x, y, w, h, radius, fill=1, stroke=1)

#     def draw_text(x, y, text, size=11, color=black, font="Helvetica"):
#         p.setFillColor(color)
#         p.setFont(font, size)
#         p.drawString(x, y, str(text))

#     def draw_fit_text(x, y, text, max_width, size=11, color=black, font="Helvetica"):
#         p.setFillColor(color)
#         p.setFont(font, size)
#         text = str(text)
#         while p.stringWidth(text, font, size) > max_width and len(text) > 3:
#             text = text[:-4] + "..."
#         p.drawString(x, y, text)

#     def draw_multiline_text(x, y, text, max_width=470, size=11, line_gap=16, color=black, font="Helvetica"):
#         p.setFillColor(color)
#         p.setFont(font, size)

#         words = str(text).split()
#         lines = []
#         current = ""

#         for word in words:
#             test = word if current == "" else current + " " + word
#             if p.stringWidth(test, font, size) <= max_width:
#                 current = test
#             else:
#                 if current:
#                     lines.append(current)
#                 current = word

#         if current:
#             lines.append(current)

#         current_y = y
#         for line in lines:
#             p.drawString(x, current_y, line)
#             current_y -= line_gap

#         return current_y

#     def draw_preline_block(title, text, x, y, w, h):
#         draw_rounded_box(x, y - h, w, h)
#         draw_text(x + 14, y - 26, title, size=14, color=black, font="Helvetica-Bold")

#         lines = str(text).splitlines()
#         current_y = y - 50
#         p.setFont("Helvetica", 10)
#         p.setFillColor(HexColor("#374151"))

#         for line in lines:
#             if current_y < (y - h + 18):
#                 break
#             p.drawString(x + 16, current_y, line)
#             current_y -= 15

#     # ===== HEADER =====
#     p.setFillColor(blue)
#     p.rect(15, height - 180, width - 30, 160, fill=1, stroke=0)

#     # Logo box
#     logo_x = 35
#     logo_y = height - 160
#     logo_w = 90
#     logo_h = 90

#     if job.company_logo:
#         logo_path = os.path.join(settings.MEDIA_ROOT, job.company_logo.name)
#         if os.path.exists(logo_path):
#             p.setFillColor(white)
#             p.roundRect(logo_x, logo_y, logo_w, logo_h, 10, fill=1, stroke=0)
#             logo = ImageReader(logo_path)
#             p.drawImage(logo, logo_x + 6, logo_y + 6, width=logo_w - 12, height=logo_h - 12, preserveAspectRatio=True, mask='auto')

#     # Title and company
#     draw_fit_text(145, height - 72, job.job_title, 260, size=21, color=white, font="Helvetica-Bold")
#     draw_text(145, height - 98, job.company_name, size=13, color=white, font="Helvetica-Bold")

#     # Website
#     website_y = height - 118
#     if getattr(job.recruiter, "company_website", None):
#         draw_fit_text(145, website_y, f"{job.recruiter.company_website}", 300, size=10, color=white, font="Helvetica")
#     else:
#         website_y += 8

#     # Job type badge
#     badge_y = height - 146
#     p.setFillColor(HexColor("#60a5fa"))
#     p.roundRect(145, badge_y, 62, 18, 9, fill=1, stroke=0)
#     p.setFillColor(white)
#     p.setFont("Helvetica-Bold", 8)
#     p.drawCentredString(176, badge_y + 6, job.get_job_type_display())

#     # Location badge
#     location_text = job.location
#     loc_w = max(70, min(120, int(p.stringWidth(location_text, "Helvetica-Bold", 8)) + 18))
#     p.setFillColor(HexColor("#60a5fa"))
#     p.roundRect(214, badge_y, loc_w, 18, 9, fill=1, stroke=0)
#     p.setFillColor(white)
#     p.setFont("Helvetica-Bold", 8)
#     p.drawString(223, badge_y + 6, location_text[:25])

#     # Rating
#     p.setFillColor(gold)
#     p.setFont("Helvetica-Bold", 10)
#     p.drawString(145, height - 168, "★ ★ ★ ★ ★")
#     p.setFillColor(white)
#     p.setFont("Helvetica", 8)
#     p.drawString(215, height - 167, "(4.8 Company Rating)")

#     # Status pill
#     status_text = "Closed" if job.is_closed else "Open"
#     status_color = red if job.is_closed else green
#     p.setFillColor(status_color)
#     p.roundRect(width - 110, height - 58, 70, 24, 12, fill=1, stroke=0)
#     p.setFillColor(white)
#     p.setFont("Helvetica-Bold", 11)
#     p.drawCentredString(width - 75, height - 49, status_text)

#     # ===== SUMMARY CARDS =====
#     card_y_top = height - 215
#     card_w = 118
#     card_h = 48
#     gap = 18
#     start_x = 40

#     # Vacancies
#     draw_rounded_box(start_x, card_y_top - card_h, card_w, card_h)
#     draw_text(start_x + 10, card_y_top - 15, "Vacancies", size=8, color=text_gray)
#     draw_text(start_x + 10, card_y_top - 35, job.vacancies, size=13, color=black, font="Helvetica-Bold")

#     # Salary
#     x2 = start_x + card_w + gap
#     draw_rounded_box(x2, card_y_top - card_h, card_w, card_h)
#     draw_text(x2 + 10, card_y_top - 15, "Salary", size=8, color=text_gray)
#     draw_fit_text(x2 + 10, card_y_top - 35, f"{job.salary} {job.currency}", 95, size=12, color=black, font="Helvetica-Bold")

#     # Opening Date
#     x3 = x2 + card_w + gap
#     draw_rounded_box(x3, card_y_top - card_h, card_w, card_h)
#     draw_text(x3 + 10, card_y_top - 15, "Opening Date", size=8, color=text_gray)
#     draw_fit_text(x3 + 10, card_y_top - 35, job.opening_date.strftime("%d %B %Y"), 100, size=10, color=black, font="Helvetica-Bold")

#     # Deadline
#     x4 = x3 + card_w + gap
#     draw_rounded_box(x4, card_y_top - card_h, card_w, card_h)
#     draw_text(x4 + 10, card_y_top - 15, "Deadline", size=8, color=text_gray)
#     draw_fit_text(x4 + 10, card_y_top - 35, job.deadline.strftime("%d %B %Y"), 100, size=10, color=(red if job.is_closed else green), font="Helvetica-Bold")

#     # Second row cards
#     card2_y_top = card_y_top - 65
#     wide_w = 160

#     # Deadline Countdown
#     draw_rounded_box(40, card2_y_top - card_h, wide_w, card_h)
#     draw_text(50, card2_y_top - 15, "Deadline Countdown", size=8, color=text_gray)

#     from django.utils import timezone
#     now_dt = timezone.now()
#     deadline_dt = timezone.datetime.combine(job.deadline, timezone.datetime.max.time(), tzinfo=now_dt.tzinfo)
#     distance = deadline_dt - now_dt

#     if distance.total_seconds() <= 0:
#         countdown_text = "Expired"
#     else:
#         days = distance.days
#         hours = distance.seconds // 3600
#         minutes = (distance.seconds % 3600) // 60
#         countdown_text = f"{days} Days {hours} Hours {minutes} Minutes"

#     draw_fit_text(50, card2_y_top - 35, countdown_text, 135, size=10, color=red, font="Helvetica-Bold")

#     # Posted On / Created Date
#     x_post = 40 + wide_w + gap
#     draw_rounded_box(x_post, card2_y_top - card_h, wide_w, card_h)
#     draw_text(x_post + 10, card2_y_top - 15, "Posted On", size=8, color=text_gray)
#     draw_fit_text(
#         x_post + 10,
#         card2_y_top - 35,
#         job.created_at.strftime("%d %B %Y, %I:%M %p"),
#         138,
#         size=9,
#         color=black,
#         font="Helvetica-Bold"
#     )

#     # Applications
#     x_app = x_post + wide_w + gap
#     draw_rounded_box(x_app, card2_y_top - card_h, wide_w, card_h)
#     draw_text(x_app + 10, card2_y_top - 15, "Applications", size=8, color=text_gray)
#     draw_text(x_app + 10, card2_y_top - 35, f"{job.applications.count()} Applicants", size=10, color=black, font="Helvetica-Bold")

#     # ===== DETAIL BOXES =====
#     details_top = card2_y_top - 70
#     box_w = 260
#     box_h = 155
#     left_x = 40
#     right_x = 310

#     draw_preline_block("Education", job.education, left_x, details_top, box_w, box_h)
#     draw_preline_block("Skills", job.skills, right_x, details_top, box_w, box_h)

#     second_row_top = details_top - box_h - 18
#     draw_preline_block("Responsibilities", job.responsibilities, left_x, second_row_top, box_w, box_h)
#     draw_preline_block("Description", job.description, right_x, second_row_top, box_w, box_h)

#     p.save()
#     return response



def download_job_pdf(request, job_id):


    if canvas is None:
        return HttpResponse("PDF feature is not available on this server.", status=503)


    job = get_object_or_404(Job, id=job_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{job.job_title}.pdf"'

    p = canvas.Canvas(response, pagesize=A4) # type: ignore

    width, height = A4 # type: ignore
    y = height - 60


    # ========= HEADER =========

    p.setFont("Helvetica-Bold", 22)
    p.drawString(60, y, job.job_title)

    p.setFont("Helvetica", 14)
    y -= 25
    p.drawString(60, y, job.company_name)

    if job.recruiter.company_website:
        y -= 18
        p.drawString(60, y, job.recruiter.company_website)


    # Status
    status = "Open" if not job.is_closed else "Closed"

    p.setFont("Helvetica-Bold", 12)
    p.drawRightString(width-60, height-60, status)


    # Company logo
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


    # ========= BASIC INFO =========

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


    # ========= TEXT SECTION FUNCTION =========

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


    # ========= DETAILS =========

    draw_section("Education", job.education)
    draw_section("Skills", job.skills)
    draw_section("Responsibilities", job.responsibilities)
    draw_section("Description", job.description)


    p.save()

    return response




from .models import JobApplication

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





# def apply_job(request, job_id):

#     job = get_object_or_404(Job, id=job_id)

#     if not request.user.is_authenticated:
#         return redirect(f"/login/?next=/job/{job.id}/")

#     if request.user.role != "job_seeker":
#         return redirect('job_detail', job_id=job.id)

#     already = JobApplication.objects.filter(
#         job=job,
#         applicant=request.user
#     ).exists()

#     if not already:
#         JobApplication.objects.create(
#             job=job,
#             applicant=request.user
#         )

#     return redirect('job_detail', job_id=job.id)
