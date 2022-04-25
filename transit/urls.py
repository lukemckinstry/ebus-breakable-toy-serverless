from django.urls import path
from .views import AgencyViewSet, RouteViewSet
from .models import Route
from rest_framework_mvt.views import mvt_view_factory

from . import views

urlpatterns = [
    path("agency/", agency_list, name="agency-list"),
    path("agency/<str:pk>/", agency_detail, name="agency-detail"),
    path("agency/<str:agency_pk>/route", route_list, name="route-list"),
    path("route/tiles", mvt_view_factory(Route)),
    path("route/<str:pk>/", route_detail, name="route-detail"),
    path("tiles/example.mvt/", mvt_view_factory(Route)),
    path("basicmap/", views.basic_map),
    path("", views.index, name="index"),
]
