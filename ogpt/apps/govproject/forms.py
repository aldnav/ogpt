from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

from .importer import importer
from .models import GovernmentProject, ProgressReport, ProjectMedia, ImportJob


class GovernmentProjectCreateForm(ModelForm):
    class Meta:
        model = GovernmentProject
        fields = "__all__"
        exclude = [
            "media_files",
            "removed",
            "is_draft",
            "is_complete",
            "completion_notes",
        ]


class CompletingProjectForm(ModelForm):
    class Meta:
        model = GovernmentProject
        fields = ["is_complete", "completion_notes"]

    # def clean_completion_notes(self):
    #     progress_report = self.instance.progress_reports.last()
    #     if len(self.cleaned_data.get('clean_completion_notes')) == 0 and progress_report is not None:
    #         return progress_report.description
    #     return self.cleaned_data.get('clean_completion_notes')

    def clean(self):
        cleaned_data = super().clean()
        is_complete = cleaned_data.get("is_complete")
        if is_complete:
            if not self.instance.progress_reports.exists():
                raise ValidationError(
                    _(
                        "At least one progress report is required to mark the project as complete!"
                    )
                )


class ProgressReportForm(ModelForm):
    when_start = forms.DateField(required=True, widget=forms.DateInput)
    same_start_end = forms.BooleanField(
        label="Same start and end",
        initial=True,
        required=False,
        widget=forms.NullBooleanSelect,
    )

    class Meta:
        model = ProgressReport
        # fields = "__all__"
        fields = (
            "author",
            "project",
            "description",
            "report_type",
            "when_start",
            "same_start_end",
            "when_end",
        )  # FIXME: Include tags
        widgets = {
            "author": forms.HiddenInput(),
            "project": forms.HiddenInput(),
            "when_end": forms.DateInput(),
        }

    def clean_when_end(self):
        if self.data.get("same_start_end"):
            self.cleaned_data["when_end"] = self.cleaned_data["when_start"]
        return self.data.get("same_start_end")


class ProjectMediaForm(ModelForm):
    class Meta:
        model = ProjectMedia
        fields = "__all__"
        widgets = {"owner": forms.HiddenInput()}


class ProgressReportChangeStatusForm(ModelForm):
    class Meta:
        model = ProgressReport
        fields = ["status"]

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if status <= self.instance.status:
            raise ValidationError(
                _("Invalid status: %(value)"), params={"value": status}
            )
        return status


from django.utils.html import format_html, format_html_join


class DivErrorList(forms.utils.ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return format_html(
            '<div class="alert alert-danger alert-dismissible fade show" role="alert">{}</div>',
            format_html_join("", "<div>{}</div>", ((e,) for e in self)),
        )


class ImportFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ".csv"}))

    def clean(self):
        cleaned_data = super().clean()
        data_file = cleaned_data.get("file")
        data_file.seek(0)
        import_response = importer.import_projects_from_csv(data_file)
        import_job = ImportJob.objects.last()
        if import_job is None:
            import_job = ImportJob.objects.create()
        import_job.data = import_response
        import_job.save()
        for error in import_response["problematic"]:
            self.add_error("file", "Line {line} : {exception}".format_map(error))
