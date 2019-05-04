import django_filters
from django.db.models import Q
from django.forms.widgets import HiddenInput
from django_filters.widgets import DateRangeWidget

from .models import GovernmentProject


class GovernmentProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains", widget=HiddenInput())
    id = django_filters.CharFilter(method="filter_id", widget=HiddenInput())
    implementation_dates = django_filters.DateFromToRangeFilter(
        label="Implementation dates",
        method="filter_implementation_dates",
        widget=DateRangeWidget(attrs={"placeholder": "YYYY/MM/DD"}),
    )

    class Meta:
        model = GovernmentProject
        fields = [
            "title",
            "total_project_cost",
            "administrative_area",
            "implementing_agency",
            "id",
        ]

    def filter_implementation_dates(self, queryset, name, value):
        filters = []
        if value:
            if value.start is not None:
                filters.append(Q(implementation_from__gte=value.start))
            if value.stop is not None:
                filters.append(Q(implementation_to__lte=value.stop))
        return queryset.filter(*filters)

    def filter_id(self, queryset, name, value):
        return queryset.filter(id__in=value.split(","))
