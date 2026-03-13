from django.urls import path
from . import views

urlpatterns = [
    path("create_new_jobs/", views.create_new_jobs, name="create_new_jobs"),
    path("analytics/", views.recruiter_dashboard_analytics, name="recruiter_analytics"),
    path("applicants/<int:job_id>/", views.job_applicant_list, name="job_applicant_list"),
    path("search-suggestions/", views.job_search_suggestions, name="job_search_suggestions"),

    path('job/view/<int:job_id>/', views.view_job, name='view_job'),
    path('job/edit/<int:job_id>/', views.edit_job, name='edit_job'),
    path('job/delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path("job/download/<int:job_id>/", views.download_job_pdf, name="download_job_pdf"),

]