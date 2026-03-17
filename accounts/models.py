from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )

    phone = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class RecruiterProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    job_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        default="Senior HR Manager"
    )

    location = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        default="Dhaka, Bangladesh"
    )

    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_website = models.URLField(max_length=255, blank=True, null=True)

    company_overview = models.TextField(
        blank=True,
        null=True,
        default="Tech Solutions Ltd. is a fast-growing software company specializing in enterprise systems, mobile apps, and cloud services."
    )

    def __str__(self):
        return f"RecruiterProfile: {self.user.username}"


class JobSeekerProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        default="Frontend Developer"
    )

    location = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        default="Dhaka, Bangladesh"
    )

    summary = models.TextField(
        blank=True,
        null=True,
        default="Passionate frontend developer with strong knowledge of HTML, CSS, Tailwind, JavaScript, and React. Looking for opportunities to build modern web apps."
    )

    skills = models.TextField(
        blank=True,
        null=True,
        default="HTML CSS Tailwind JavaScript React"
    )

    experience = models.TextField(
        blank=True,
        null=True,
        default="Junior Web Developer — ABC Tech\n2024 - Present\nWorked on responsive UI, landing pages, and dashboard interfaces."
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="+880 1234-567890"
    )

    linkedin = models.URLField(
        blank=True,
        null=True,
        default="https://linkedin.com/in/officialontar"
    )

    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"JobSeekerProfile: {self.user.username}"


class Application(models.Model):

    job = models.ForeignKey(
        "jobs.Job",
        related_name="applications",
        on_delete=models.CASCADE
    )

    applicant = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} applied to {self.job}"
