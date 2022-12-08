from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from siptrack_fetch import views as siptrack_views
from api import passwordstate as ps_views


class PublicEndpoint(BasePermission):

    def has_permission(self, request, view):
        return True


class FetchPasswords(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        context = dict()
        context['result'] = siptrack_views.fetch_paswords()
        return Response(context)


class DataAdd(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        context = dict()
        context['result'] = siptrack_views.add_data()
        return Response(context)


class AddTreeData(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        context = dict()
        context['result'] = siptrack_views.add_tree_details()
        return Response(context)


class DeviceFetch(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (PublicEndpoint,)

    def get(self, request, device_oid):
        context = dict()
        context['result'] = siptrack_views.fetch(device_oid)
        return Response(context)


class DeviceFetchAll(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        context = dict()
        context['result'] = siptrack_views.fetchall()
        return Response(context)


class CreateFolder(APIView):
    parser_classes = (JSONParser,)
    permission_classes = (PublicEndpoint,)

    def get(self, request, ):
        context = dict()
        context['result'] = ps_views.create_folder()
        return Response(context)