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
                    "<slug:slug>/",
                    views.GovernmentProjectDetailView.as_view(),
                    name="govproject.GovernmentProjectDetailView",
                ),
            ]
        ),
    ),
]
