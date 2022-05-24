"""
Contains the user profile view
"""

from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated

from ..models import CustomUser
from ..serializers import FullUserSerializer


class Profile(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView):
    """
    Get or update the current user profile
    """

    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all()
    serializer_class = FullUserSerializer

    def get_object(self):
        """
        Fetch the user details object for the logged-in user
        """
        return self.queryset.get(pk=self.request.user.id)

    def get(self, request, *args, **kwargs):
        """
        Get the details of the current user
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update the details of the current user
        """
        return self.update(request, *args, **kwargs)
