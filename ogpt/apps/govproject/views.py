from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin

from django_filters.views import FilterView
from django_tables2.paginators import LazyPaginator
from django_tables2.views import SingleTableMixin
from rest_framework import generics, mixins
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from .forms import GovernmentProjectCreateForm, ProgressReportForm
from .filtersets import GovernmentProjectFilter
from .models import GovernmentProject, ProgressReport
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


class GovernmentProjectDetailView(SuccessMessageMixin, FormMixin, DetailView):
    model = GovernmentProject
    template_name = "govproject/projects_detail.html"

    http_method_names = ['get', 'post']
    form_class = ProgressReportForm
    prefix = 'PR'

    success_message = "A progress report was added successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['progress_reports'] = self.get_object().progress_reports.order_by('-timestamp')
        return context

    def get_initial(self):
        return dict(
            project=self.get_object(),
            author=self.request.user,
        )

    def get_success_url(self):
        return reverse_lazy(
            'govproject.GovernmentProjectDetailView',
            args=(self.get_object().slug,)
        ) + '#progress'

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
