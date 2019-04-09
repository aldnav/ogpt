import django_tables2 as tables

from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.html import mark_safe

from .models import GovernmentProject


class GovernmentProjectTable(tables.Table):
    title = tables.Column("Project")
    # description = tables.Column(orderable=False)
    implementing_agency = tables.Column()
    total_project_cost = tables.Column()
    funding_source = tables.Column("Source of funding")
    implementation_time_info = tables.Column("Implementation Period")
    # administrative_area = tables.Column(empty_values=())

    def render_title(self, record, value):
        return mark_safe(
            '<a href="{0.url}"><span class="status status-{0.status}" title="{0.status}"></span>&nbsp;{0.title}</a>'.format(record)
        )

    def render_total_project_cost(self, record, value):
        return intcomma(value)

    def render_administrative_area(self, record, value):
        return ",".join(record.administrative_area.all().values_list("name", flat=True))

    # class Meta:
    #     model = GovernmentProject
