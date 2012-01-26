from django.contrib import admin
from copwatch.incident.models import Cop, Incident, Force



admin.site.register(Cop)
admin.site.register(Incident)
admin.site.register(Force)
