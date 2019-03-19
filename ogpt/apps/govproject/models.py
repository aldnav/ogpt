from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class GovernmentProject(models.Model):
    title = models.CharField(max_length=255, help_text="The title of the project")
    description = models.TextField(
        blank=True,
        help_text="Describes the purpose of the project, "
        "the main beneficiaries and may include "
        "a short text of the proposal",
    )
    total_project_cost = models.FloatField(
        null=True, blank=True, help_text="The Total Project Cost on record"
    )
    implementing_agency = models.ForeignKey(
        "Agency",
        related_name="projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Agency in charge",
    )
    implementation_period = models.DurationField(
        null=True, blank=True, help_text="Duration of the project"
    )
    # When implementation period is unknown
    # provide a way to indicate start and end
    implementation_from = models.DateTimeField(
        null=True, blank=True, help_text="Start datetime of implementation"
    )
    implementation_to = models.DateTimeField(
        null=True, blank=True, help_text="End datetime of implementation"
    )
    funding_source = models.ForeignKey(
        "FundingSource",
        related_name="projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Source of funding",
    )
    administrative_area = models.ManyToManyField(
        "Region", related_name="projects", help_text="Target region of the project"
    )

    class Meta:
        app_label = "govproject"
        ordering = ("pk",)

    def __str__(self):
        return self.title

    @property
    def implementation_time_info(self):
        implementation_time_info = self.implementation_period
        if self.implementation_period is None:
            implementation_time_info = "{0.implementation_from} - {0.implementation_to}".format(
                self
            )
        return implementation_time_info


class ICCDate(models.Model):
    timestamp = models.DateTimeField(help_text="Datetime of ICCDate instance")
    description = models.CharField(
        max_length=180, help_text="Optional: Short text describing the date"
    )

    class Meta:
        abstract = True


class ICCTBDate(ICCDate):
    """ICC-Techincal Board date"""

    project = models.ForeignKey(
        GovernmentProject,
        related_name="icc_tb_dates",
        on_delete=models.CASCADE,
        help_text="Reference to project",
    )


class ICCCCDate(ICCDate):
    """ICC-Cabinet Committee date"""

    project = models.ForeignKey(
        GovernmentProject,
        related_name="icc_cc_dates",
        on_delete=models.CASCADE,
        help_text="Reference to project",
    )


class Agency(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the agency")
    shortname = models.CharField(max_length=180, blank=True, help_text="Abbreviation")

    def __str__(self):
        return "{0.name} - {0.shortname}".format(self)


class ProjectLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=510)
    added_by = models.ForeignKey(
        User,
        related_name="added_logs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):

        return "{0.timestamp} - {0.label} - {0.added_by.full_name}".format(self)


class Region(models.Model):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(
        "Latitude", max_digits=18, decimal_places=12, blank=True, null=True
    )
    lng = models.DecimalField(
        "Longitude", max_digits=18, decimal_places=12, blank=True, null=True
    )

    def __str__(self):
        return self.name


class FundingSource(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the funding source")

    def __str__(self):
        return self.name


class ProgressReport(models.Model):
    author = models.ForeignKey(
        User,
        related_name="added_reports",
        default=settings.ANONYMOUS_USER,
        on_delete=models.SET_DEFAULT,
        help_text=_("The author of the report"),
    )
    project = models.ForeignKey(
        GovernmentProject,
        related_name="progress_reports",
        on_delete=models.CASCADE,
        help_text=_("The project to which this report is for"),
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    when_start = models.DateTimeField(
        help_text=_("Defaults to datetime added"), auto_now_add=True
    )
    when_end = models.DateTimeField(
        help_text=_("Defaults to datetime added"), auto_now_add=True
    )
    description = models.TextField(help_text=_("Describe what the report is about"))

    SUPPLEMENTAL = 0
    BLOCKER = 1
    DISCONTINUED = 2
    REPORT_TYPES = (
        (SUPPLEMENTAL, "SUPPLEMENTAL"),
        (BLOCKER, "BLOCKER"),
        (DISCONTINUED, "DISCONTINUED"),
    )
    report_type = models.IntegerField(
        choices=REPORT_TYPES,
        default=SUPPLEMENTAL,
        help_text=_(
            "'Supplemental' are for normal reports. "
            "'Blocker' indicates obstacles in progressing the project. "
            "While 'Discontinued' flags a project as incomplete."
        ),
    )

    def __str__(self):
        return "Project-{0.project.pk} - Report: {0.pk} - By: {0.author}".format(self)
