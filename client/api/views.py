
from rest_framework import mixins
from rest_framework.permissions import (IsAdminUser, 
                                    IsAuthenticated, 
                                    AllowAny,
                                    IsAuthenticatedOrReadOnly)
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import (ListAPIView, 
                                    CreateAPIView,
                                    RetrieveAPIView,
                                    GenericAPIView,)

from .serializers import (UserSerializer,
                        UserDetailSerializer, 
                        UserCreateSerializer,
                        UserLoginSerializer)

from rest_framework.response import Response 
from rest_framework.status import (HTTP_200_OK, 
                                HTTP_400_BAD_REQUEST, 
                                HTTP_204_NO_CONTENT)
from rest_framework.views import APIView 


from django.contrib.auth import get_user_model
User = get_user_model()


class UserListView(ListAPIView):
    """
    API for list of users for admin.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UserDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    GenericAPIView):
    """
    API for detail of users for owner.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserCreateAPIView(mixins.CreateModelMixin,
                        GenericAPIView):
    """
    API for create of users.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    
class UserLoginAPIView(APIView):
    """
    API for login users.
    """
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data =  request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)