from django.db import models
from django.utils import timezone
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

    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)

    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    company_website = models.URLField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logo/', null=True, blank=True)

    responsibilities = models.TextField()
    education = models.TextField()
    vacancies = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default='BDT'
    )

    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    skills = models.TextField()
    opening_date = models.DateField()
    deadline = models.DateField()
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_closed(self):
        return self.deadline < timezone.localdate()

    @property
    def status_text(self):
        return "Closed" if self.is_closed else "Open"

    def __str__(self):
        return self.job_title