import django_filters

from .models import GovernmentProject


class GovernmentProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = GovernmentProject
        fields = ["title", "total_project_cost", "administrative_area"]
