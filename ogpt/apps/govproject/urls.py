from django.urls import include, path
from . import views

urlpatterns = [
    path(
        "",
        views.GovernmentProjectListView.as_view(),
        name="govproject.GovernmentProjectListView",
    ),
    path(
        "projects/",
        include(
            [
                path(
                    "create/",
                    views.GovernmentProjectCreateView.as_view(),
                    name="govproject.GovernmentProjectCreateView",
                ),
                path(
                    "media/",
                    views.ProjectMediaFormView.as_view(),
                    name="govproject.ProjectMediaFormView",
                ),
                path(
                    "<slug:slug>/edit/",
                    views.GovernmentProjectEditView.as_view(),
                    name="govproject.GovernmentProjectEditView",
                ),
                path(
                    "<slug:slug>/remove/",
                    views.GovernmentProjectRemoveView.as_view(),
                    name="govproject.GovernmentProjectRemoveView",
                ),
                path(
                    "<slug:slug>/",
                    views.GovernmentProjectDetailView.as_view(),
                    name="govproject.GovernmentProjectDetailView",
                ),
            ]
        ),
    ),
]
