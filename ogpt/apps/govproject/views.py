from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, UpdateView, FormView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from django_tables2.paginators import LazyPaginator
from django_tables2.views import SingleTableMixin
from rest_framework import generics, mixins
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from apps.django_tables_extensions.export import SerializerExportMixin
from .filtersets import GovernmentProjectFilter
from .forms import (
    GovernmentProjectCreateForm,
    ProgressReportForm,
    ProjectMediaForm,
    ProgressReportChangeStatusForm,
)
from .forms import ImportFileForm, DivErrorList, CompletingProjectForm
from .models import GovernmentProject, Region, ProgressReport, ImportJob
from .serializers import GovernmentProjectSerializer
from .tables import GovernmentProjectTable

default_renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
from django.db.models import Sum


class GovernmentProjectListView(
    mixins.ListModelMixin,
    SerializerExportMixin,
    SingleTableMixin,
    FilterView,
    generics.GenericAPIView,
):
    queryset = GovernmentProject.objects.filter(removed=False, is_draft=False)
    serializer_class = GovernmentProjectSerializer
    renderer_classes = default_renderer_classes
    template_name = "govproject/projects_list.html"
    table_class = GovernmentProjectTable
    filterset_class = GovernmentProjectFilter
    paginate_by = 10
    paginator_class = LazyPaginator
    export_name = "projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_administrative_area = self.request.GET.get("administrative_area", [])
        if len(selected_administrative_area) == 0:
            admin_areas = Region.objects.all()
        else:
            admin_areas = Region.objects.filter(pk__in=selected_administrative_area)
        context["administrative_areas"] = admin_areas
        headlines = dict(
            count_admin_areas=Region.objects.count(),
            count_projects=GovernmentProject.objects.exclude(is_draft=True).count(),
            count_funds=GovernmentProject.objects.aggregate(
                total_funds=Sum("total_project_cost")
            )["total_funds"],
        )
        context.update(headlines)
        return context


class GovernmentProjectDraftListView(GovernmentProjectListView):
    extra_context = {
        "announcement": _(
            "* These are <b>draft</b> projects. Publish them individually."
        )
    }

    def get_queryset(self):
        return GovernmentProject.objects.filter(removed=False, is_draft=True)


class GovernmentProjectCreateView(SuccessMessageMixin, CreateView):
    form_class = GovernmentProjectCreateForm
    template_name = "govproject/projects_create.html"
    success_url = "/"
    success_message = "%(title)s was added successfully"


class GovernmentProjectEditView(SuccessMessageMixin, UpdateView):
    model = GovernmentProject
    queryset = GovernmentProject.objects.filter(is_complete=False)
    form_class = GovernmentProjectCreateForm
    template_name = "govproject/projects_create.html"
    success_message = "%(title)s edited!"
    extra_context = {"user_action": "Edit"}

    def get_success_url(self):
        return self.object.url

    def form_valid(self, form):
        self.object = form.save()
        if self.request.POST.get("submit") == "submit_and_publish":
            self.object.is_draft = False
            self.object.save(update_fields=["is_draft"])
            messages.info(
                self.request, _("{0.title} is published!".format(self.object))
            )
        return super().form_valid(form)


class GovernmentProjectRemoveView(DetailView):
    model = GovernmentProject
    queryset = GovernmentProject.objects.filter(removed=False)
    template_name = "govproject/projects_remove.html"
    success_message = "{0.id} - {0.title} deleted!"

    def get_success_url(self):
        return reverse_lazy("govproject.GovernmentProjectListView")

    def post(self, request, *args, **kwargs):
        if self.request.POST.get("delete") == "1":
            project = self.get_object()
            project.removed = True
            project.save()
            messages.success(request, message=self.success_message.format(project))
            return HttpResponseRedirect(self.get_success_url())
        return self.get(request, *args, **kwargs)


class GovernmentProjectDetailView(SuccessMessageMixin, FormMixin, DetailView):
    model = GovernmentProject
    queryset = GovernmentProject.objects.filter(removed=False)
    template_name = "govproject/projects_detail.html"

    http_method_names = ["get", "post"]
    form_class = ProgressReportForm
    prefix = "PR"

    def get_queryset(self):
        if not self.request.user.has_perm("sites.frontend_access"):
            return self.queryset.filter(is_draft=False)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        progress_reports = (
            self.get_object()
            .progress_reports.exclude(when_start__isnull=True)
            .order_by("-when_start", "-timestamp")
        )
        if not self.request.user.has_perm("sites.frontend_access"):
            progress_reports = progress_reports.filter(status=ProgressReport.APPROVED)
        context["progress_reports"] = progress_reports
        context["media_form"] = ProjectMediaForm(initial={"owner": self.request.user})
        return context

    def get_initial(self):
        return dict(project=self.get_object(), author=self.request.user)

    def get_success_url(self):
        return (
            reverse_lazy(
                "govproject.GovernmentProjectDetailView", args=(self.get_object().slug,)
            )
            + "#progress"
        )

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        if self.request.POST.get("accepts") == "media":
            self.handle_media_form(request, *args, **kwargs)
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, "Progress report created!")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def handle_media_form(self, request, *args, **kwargs):
        media_form = ProjectMediaForm(request.POST, request.FILES)
        if media_form.is_valid():
            media = media_form.save()
            self.object.media_files.add(media)
            messages.success(request, "Media file created!")
            return self.form_valid(media_form)
        else:
            messages.error(request, media_form.errors)
            return self.form_invalid(media_form)


class ProjectMediaFormView(CreateView):
    form_class = ProjectMediaForm
    template_name = "govproject/project_media_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_slug = self.request.GET.get("project")
        self.project = get_object_or_404(
            GovernmentProject, slug=project_slug, removed=False
        )
        return context

    def get_success_url(self):
        return self.project.url


class ChangeStatusMixin(SuccessMessageMixin):
    model = ProgressReport
    form_class = ProgressReportChangeStatusForm
    template_name = "govproject/reports_change_status.html"

    def get_success_url(self):
        return self.object.project_url + "#progress"

    def get_success_message(self, cleaned_data):
        return "Report {} is getting {}!".format(
            self.object.pk, self.object.get_status_display().lower()
        )


class ReportVerifyView(ChangeStatusMixin, UpdateView):
    queryset = ProgressReport.objects.filter(status=ProgressReport.INITIAL)
    extra_context = {"user_action": "verify", "next_status": ProgressReport.VERIFIED}


class ReportApproveView(ChangeStatusMixin, UpdateView):
    queryset = ProgressReport.objects.filter(status=ProgressReport.VERIFIED)
    extra_context = {"user_action": "approve", "next_status": ProgressReport.APPROVED}


class ProjectImportView(FormView):
    template_name = "govproject/project_import.html"
    form_class = ImportFileForm

    def get_form_kwargs(self):
        kwargs = super(ProjectImportView, self).get_form_kwargs()
        kwargs.update(error_class=DivErrorList)
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Projects are being imported!")
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(import_job=ImportJob.objects.last())
        return context


class ProjectCompletingView(SuccessMessageMixin, UpdateView):
    template_name = "govproject/project_completing.html"
    form_class = CompletingProjectForm
    queryset = GovernmentProject.objects.filter(is_complete=False)
    success_message = "Project is marked complete!"

    def get_success_url(self):
        return self.object.url
