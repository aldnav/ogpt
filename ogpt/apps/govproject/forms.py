from django.forms import ModelForm
from .models import GovernmentProject, ProgressReport


class GovernmentProjectCreateForm(ModelForm):
    class Meta:
        model = GovernmentProject
        fields = "__all__"


class ProgressReportForm(ModelForm):
    class Meta:
        model = ProgressReport
        fields = "__all__"
