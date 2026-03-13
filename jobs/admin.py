from django.contrib import admin
from .models import Job

# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "job_title",
        "company_name",
        "vacancies",
        "salary",
        "currency",
        "job_type",
        "location",
        "deadline",
        "created_at",
    )

    search_fields = (
        "job_title",
        "company_name",
        "location",
    )

    list_filter = (
        "job_type",
        "currency",
        "deadline",
    )