import django_tables2 as tables
from .models import GovernmentProject


class GovernmentProjectTable(tables.Table):
    title = tables.Column(attrs={"td": {"nowrap": True}})
    description = tables.Column(attrs={"th": {"width": "400px"}})
    total_project_cost = tables.Column()

    # class Meta:
    #     model = GovernmentProject
