from django.forms import ModelForm
from .models import GovernmentProject


class GovernmentProjectCreateForm(ModelForm):
    class Meta:
        model = GovernmentProject
        fields = "__all__"
