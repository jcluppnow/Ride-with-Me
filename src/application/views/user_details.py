# pylint:disable=invalid-name
"""
Contains the user details view
"""

from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from ..models import CustomUser
from ..serializers import BasicUserSerializer


@api_view()
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.AllowAny])
def user_details(request, pk):
    """
    Get the details for an individual user (with private information redacted)
    """
    queryset = CustomUser.objects.get(pk=pk)
    serializer = BasicUserSerializer(queryset)
    return Response(serializer.data)
