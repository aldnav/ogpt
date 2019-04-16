from django.core.exceptions import ImproperlyConfigured
from django_tables2.export import ExportMixin
from django_tables2.export.export import TableExport

try:
    from tablib import Dataset
except ImportError:  # pragma: no cover
    raise ImproperlyConfigured(
        "You must have tablib installed in order to use the django-tables2 export functionality"
    )


class SerializerTableExport(TableExport):
    def __init__(self, export_format, table, serializer=None, exclude_columns=None):
        if not self.is_valid_format(export_format):
            raise TypeError(
                'Export format "{}" is not supported.'.format(export_format)
            )

        self.format = export_format
        if serializer is None:
            raise TypeError("Serializer should be provided for table {}".format(table))

        self.dataset = Dataset()
        serializer_data = serializer([x for x in table.data], many=True).data
        if len(serializer_data) > 0:
            self.dataset.headers = serializer_data[0].keys()
        for row in serializer_data:
            self.dataset.append(row.values())


class SerializerExportMixin(ExportMixin):
    def create_export(self, export_format):
        exporter = SerializerTableExport(
            export_format=export_format,
            table=self.get_table(**self.get_table_kwargs()),
            serializer=self.serializer_class,
            exclude_columns=self.exclude_columns,
        )

        return exporter.response(filename=self.get_export_filename(export_format))

    def get_serializer(self, table):
        if self.serializer_class is not None:
            return self.serializer_class
        else:
            return getattr(
                self, "{}Serializer".format(self.get_table().__class__.__name__), None
            )

    def get_table_data(self):
        selected_column_ids = self.request.GET.get("_selected_column_ids", None)
        if selected_column_ids:
            selected_column_ids = map(int, selected_column_ids.split(","))
            return super().get_table_data().filter(id__in=selected_column_ids)
        return super().get_table_data()
