from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import (
    BrowsableAPIRenderer,
    JSONRenderer,
    HTMLFormRenderer,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Incident
from .serializers import IncidentSerializer, ReporterSerializer
from .services import (
    get_incident_by_id,
    create_incident_postscript,
    update_incident_status,
    update_incident_severity,
    get_reporter_by_id
)

class IncidentResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'pageSize'
    max_page_size = 100

class IncidentList(APIView, IncidentResultsSetPagination):
    # authentication_classes = (JSONWebTokenAuthentication, )
    # permission_classes = (IsAuthenticated,)

    serializer_class = IncidentSerializer

    def get_paginated_response(self, data):
        return Response(dict([
            ('pages', self.page.paginator.count),
            ('pageNumber', self.page.number),
            ('incidents', data)
        ]))

    def get(self, request, format=None):
        incidents = Incident.objects.all()
        results = self.paginate_queryset(incidents, request, view=self)
        serializer = IncidentSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = IncidentSerializer(data=request.data)
        if serializer.is_valid():
            incident = serializer.save()
            create_incident_postscript(incident, request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncidentDetail(APIView):
    serializer_class = IncidentSerializer

    def get(self, request, incident_id, format=None):
        incident = get_incident_by_id(incident_id)

        if incident is None:
            return Response("Invalid incident id", status=status.HTTP_404_NOT_FOUND)

        serializer = IncidentSerializer(incident)
        return Response(serializer.data)

    def put(self, request, incident_id, format=None):
        snippet = get_incident_by_id(incident_id)
        serializer = IncidentSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncidentStatusView(APIView):
    def get(self, request, incident_id, format=None):
        if not ( request.user.has_perm("incidents.can_request_status_change") or 
                 request.user.has_perm("incidents.can_change_status") ):
                 return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        action = request.GET.get("action")

        incident = get_incident_by_id(incident_id)

        if incident is None:
            return Response("Invalid incident id", status=status.HTTP_404_NOT_FOUND)

        if action:
            if action == "update":
                status_type = request.GET.get("type")
                result = update_incident_status(incident, request.user, status_type)

                if result[0] == "success":
                    return Response(result[1])
                elif result[0] == "error":
                    return Response(result[1], status=status.HTTP_400_BAD_REQUEST)

            return Response("Invalid action", status=status.HTTP_400_BAD_REQUEST)
        return Response("No action defined", status=status.HTTP_400_BAD_REQUEST)


class IncidentSeverityView(APIView):
    def get(self, request, incident_id, format=None):
        if not ( request.user.has_perm("incidents.can_request_severity_change") or 
                 request.user.has_perm("incidents.can_change_severity") ):
                 return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        action = request.GET.get("action")

        incident = get_incident_by_id(incident_id)

        if incident is None:
            return Response("Invalid incident id", status=status.HTTP_404_NOT_FOUND)

        if action:
            if action == "update":
                severity_type = request.GET.get("type")
                result = update_incident_severity(incident, request.user, severity_type)

                if result[0] == "success":
                    return Response(result[1])
                elif result[0] == "error":
                    return Response(result[1], status=status.HTTP_400_BAD_REQUEST)

            return Response("Invalid action", status=status.HTTP_400_BAD_REQUEST)
        return Response("No action defined", status=status.HTTP_400_BAD_REQUEST)

class ReporterDetail(APIView):
    serializer_class = ReporterSerializer

    def get(self, request, reporter_id, format=None):
        reporter = get_reporter_by_id(reporter_id)

        if reporter is None:
            return Response("Invalid reporter id", status=status.HTTP_404_NOT_FOUND)

        serializer = ReporterSerializer(reporter)
        return Response(serializer.data)

    def put(self, request, reporter_id, format=None):
        snippet = get_reporter_by_id(reporter_id)
        serializer = ReporterSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)