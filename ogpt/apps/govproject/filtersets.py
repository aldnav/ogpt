from django_filters.widgets import DateRangeWidget
import django_filters

from django.db.models import Q


from .models import GovernmentProject


class GovernmentProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
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
        ]

    def filter_implementation_dates(self, queryset, name, value):
        filters = []
        if value:
            if value.start is not None:
                filters.append(Q(implementation_from__gte=value.start))
            if value.stop is not None:
                filters.append(Q(implementation_to__lte=value.stop))
        return queryset.filter(*filters)
