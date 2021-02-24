from django.contrib import admin

from apps.company.models import Company, WorkerProfile

admin.site.register(Company)
admin.site.register(WorkerProfile)

