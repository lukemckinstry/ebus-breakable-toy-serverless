from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .serializers import AgencySerializer, RouteSerializer
from .models import Agency, Route
from rest_framework import viewsets, permissions


def index(request):
    return HttpResponse("Hello, world. You're at the routes index.")


def basic_map(request):
    # return basic map

    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    return render(request, "transit/index.html")


def route_bbox(request, pk):
    r = Route.objects.get(id=pk).mpoly.extent
    return JsonResponse({"bbox": r})


class AgencyViewSet(viewsets.ModelViewSet):
    """
    Viewset to automatically provide the `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Agency.objects.all()
    serializer_class = AgencySerializer


class RouteViewSet(viewsets.ModelViewSet):
    """
    Viewset to automatically provide the `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agency = self.kwargs.get("agency_pk")  # supports get request by agency endpoint
        if not agency:
            return Route.objects.all()  # all other requests
        queryset = Route.objects.filter(agency=agency)
        return queryset
