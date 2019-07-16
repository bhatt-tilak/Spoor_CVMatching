### admin.py contains the admin privileges
## here databases are registered so that the admin can view and edit them
#



from django.contrib import admin
from . models import Applicant, Job, JobApplicant
# Register your models here.

admin.site.register(Candidate)
admin.site.register(Vacancy)
admin.site.register(JobApplicant)