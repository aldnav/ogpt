from django.contrib import admin

from .models import GovernmentProject, Region, ProjectLog


@admin.register(GovernmentProject)
class GovernmentProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectLog)
class ProjectLog(admin.ModelAdmin):
    pass
