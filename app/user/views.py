from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer
from core import models


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


# view for API validating user credentials and providing token
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    # class that will render this page
    # works without this but does not create nice view in the browser
    # as it did when extended from generic views
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# view for API retrieving and updating user info
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    # queryset = models.User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user

    # retrieve and return "authenticated" user
    # this method is also required for update (patch)
    def get_object(self):
        """authentication class assigns user to request"""
        return self.request.user