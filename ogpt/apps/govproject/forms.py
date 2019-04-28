from django import forms
from django.forms import ModelForm
from .models import GovernmentProject, ProgressReport, ProjectMedia


class GovernmentProjectCreateForm(ModelForm):
    class Meta:
        model = GovernmentProject
        fields = "__all__"
        exclude = ["media_files"]


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
