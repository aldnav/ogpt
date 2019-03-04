from django.urls import path
from . import views

urlpatterns = [path("", views.GovernmentProjectListView.as_view())]
