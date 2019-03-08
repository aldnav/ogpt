import django_tables2 as tables
from .models import GovernmentProject


class GovernmentProjectTable(tables.Table):
    title = tables.Column()
    description = tables.Column()
    implementing_agency = tables.Column()
    total_project_cost = tables.Column()
    funding_source = tables.Column("Source of funding")
    implementation_time_info = tables.Column("Implementation Period")
    administrative_area = tables.Column(empty_values=())

    def render_administrative_area(self, record, value):
        return ",".join(record.administrative_area.all().values_list("name", flat=True))

    # class Meta:
    #     model = GovernmentProject
