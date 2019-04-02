from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

from django_filters.views import FilterView
from django_tables2.paginators import LazyPaginator
from django_tables2.views import SingleTableMixin
from rest_framework import generics, mixins
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from .forms import GovernmentProjectCreateForm
from .filtersets import GovernmentProjectFilter
from .models import GovernmentProject
from .serializers import GovernmentProjectSerializer
from .tables import GovernmentProjectTable


default_renderer_classes = (TemplateHTMLRenderer, JSONRenderer)


class GovernmentProjectListView(
    mixins.ListModelMixin, SingleTableMixin, FilterView, generics.GenericAPIView
):
    queryset = GovernmentProject.objects.all()
    serializer_class = GovernmentProjectSerializer
    renderer_classes = default_renderer_classes
    template_name = "govproject/projects_list.html"
    table_class = GovernmentProjectTable
    filterset_class = GovernmentProjectFilter
    paginate_by = 10
    paginator_class = LazyPaginator


class GovernmentProjectCreateView(SuccessMessageMixin, CreateView):
    form_class = GovernmentProjectCreateForm
    template_name = "govproject/projects_create.html"
    success_url = "/"
    success_message = "%(title)s was added successfully"


class GovernmentProjectDetailView(DetailView):
    model = GovernmentProject
    template_name = "govproject/projects_detail.html"
