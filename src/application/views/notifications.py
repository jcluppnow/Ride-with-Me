# pylint:disable=invalid-name
"""
Contains the notifications views
"""
from django.utils import timezone
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from ..models import Notification
from ..serializers import NotificationSerializer


@api_view(['GET', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def notifications(request):
    """
    Get all of a user's unread notifications
    """

    if request.method == 'GET':
        queryset = Notification.objects.filter(
            recipient=request.user,
            read_at=None
        )

        serializer = NotificationSerializer(
            queryset,
            many=True
        )

        return Response(serializer.data)

    if request.method == 'DELETE':
        # Mark all notifications as read
        Notification.objects.filter(
            recipient=request.user,
            read_at=None
        ).update(read_at=timezone.now())

        return Response(
            status=HTTP_204_NO_CONTENT
        )

    return None

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def notification(request, pk):
    """
    Mark a particular notification as read
    """
    Notification.objects.get(pk=pk)\
        .update(read_at=timezone.now())

    return Response(
        status=HTTP_204_NO_CONTENT
    )
