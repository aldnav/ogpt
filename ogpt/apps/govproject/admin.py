from django.contrib import admin

from .models import (
    GovernmentProject,
    Region,
    ProjectLog,
    Agency,
    FundingSource,
    ProgressReport,
    ProjectMedia,
    ImportJob,
)


@admin.register(GovernmentProject)
class GovernmentProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectLog)
class ProjectLogAdmin(admin.ModelAdmin):
    pass


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    pass


@admin.register(FundingSource)
class FundingSourceAdmin(admin.ModelAdmin):
    pass


@admin.register(ProgressReport)
class ProgressReport(admin.ModelAdmin):
    pass


@admin.register(ProjectMedia)
class ProjectMediaAdmin(admin.ModelAdmin):
    pass


@admin.register(ImportJob)
class ImportJobAdmin(admin.ModelAdmin):
    pass
