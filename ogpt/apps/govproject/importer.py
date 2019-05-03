import csv
import io
from decimal import Decimal

from apps.govproject.models import GovernmentProject


class Importer:
    valid_headers = ["title", "description", "total_project_cost"]

    @staticmethod
    def import_projects_from_csv(data):
        problematic_rows = []
        skipped = []
        created = []
        data = io.StringIO(data.read().decode("utf-8"))
        reader = csv.DictReader(data)
        line = 0
        for row in reader:
            try:
                row["total_project_cost"] = Decimal(
                    row["total_project_cost"].replace(",", "")
                )
                row_project_title = row.pop("title")
                project, is_created = GovernmentProject.objects.get_or_create(
                    title=row_project_title
                )
                if is_created:
                    for field, value in row.items():
                        setattr(project, field, value)
                    project.is_draft = True
                    project.save()
                    created.append(project.pk)
                else:
                    skipped.append(project.pk)
            except Exception as e:
                problematic_rows.append(dict(line=line, exception=str(e)))
            line += 1
        return dict(problematic=problematic_rows, skipped=skipped, created=created)


importer = Importer()
