from django_tables2 import SingleTableView
from rest_framework import generics, mixins
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from .models import GovernmentProject
from .serializers import GovernmentProjectSerializer
from .tables import GovernmentProjectTable


default_renderer_classes = (TemplateHTMLRenderer, JSONRenderer)


class GovernmentProjectListView(
    mixins.ListModelMixin, SingleTableView, generics.GenericAPIView
):
    queryset = GovernmentProject.objects.all()
    serializer_class = GovernmentProjectSerializer
    renderer_classes = default_renderer_classes
    template_name = "govproject/projects_list.html"
    table_class = GovernmentProjectTable
