from django.db import models
from django.utils import timezone
from django.conf import settings
from accounts.models import RecruiterProfile


class Job(models.Model):

    TYPE_CHOICES = [
        ('part_time', 'Part Time'),
        ('full_time', 'Full Time'),
        ('remote_job', 'Remote Job'),
    ]

    CURRENCY_CHOICES = [
        ('BDT', 'BDT ৳'),
        ('USD', 'USD $'),
        ('EURO', 'EURO €'),
        ('INR', 'INR ₹'),
    ]

    recruiter = models.ForeignKey(
        RecruiterProfile,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    company_website = models.URLField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logo/', blank=True, null=True)

    description = models.TextField()
    responsibilities = models.TextField()
    education = models.TextField()
    skills = models.TextField()

    vacancies = models.PositiveIntegerField()

    salary = models.DecimalField(max_digits=10, decimal_places=2)

    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default='BDT'
    )

    job_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    location = models.CharField(max_length=200)

    opening_date = models.DateField()
    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    # Automatic Job Status
    @property
    def is_closed(self):
        return self.deadline < timezone.localdate()

    @property
    def status(self):
        return "Closed" if self.is_closed else "Available"

    def __str__(self):
        return self.job_title


# ---------------------------------------------
# JOB APPLICATION MODEL
# ---------------------------------------------

class JobApplication(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant} applied to {self.job}"