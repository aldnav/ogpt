from rest_framework import serializers

from .models import GovernmentProject


class GovernmentProjectSerializer(serializers.ModelSerializer):
    implementing_agency = serializers.SerializerMethodField()
    funding_source = serializers.SerializerMethodField()
    administrative_area = serializers.SerializerMethodField()

    class Meta:
        model = GovernmentProject
        fields = (
            "id",
            "title",
            "description",
            "total_project_cost",
            "implementing_agency",
            "implementation_from",
            "implementation_to",
            "funding_source",
            "administrative_area",
        )

    def get_implementing_agency(self, obj):
        return obj.implementing_agency.name

    def get_funding_source(self, obj):
        return obj.funding_source.name

    def get_administrative_area(self, obj):
        return ",".join(obj.administrative_area.all().values_list("name", flat=True))
