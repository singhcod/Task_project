from django.shortcuts import render

# Create your views here.

from rest_framework import generics,permissions
from rest_framework.response import Response
from Task_app.serializers import RegisterSerializer,UserSerializer
from knox.models import AuthToken
from django.contrib.auth import login,logout
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginVew
from knox.views import LogoutAllView as KnowLogoutView

#Register APi

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view)
]

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1]
        })


class LoginApi(KnoxLoginVew):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        return super(LoginApi,self).post(request)


from Task_app.serializers import ChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class ChangePasswordApiView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        object = self.request.user
        return object

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()  # add user credentials
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            if  not self.object.check_password(serializer.data.get('old_password')): #check old password
                return Response({'old Password':'Wrong password'},status=status.HTTP_400_BAD_REQUEST)
            else:
                #update new password with old password
                self.object.set_password(serializer.data.get('new_password'))
                self.object.save()
                response = {
                    'status': 'Success',
                    'code': status.HTTP_200_OK,
                    'message': "password updated successfully",
                    'data':[]
                }
                return response
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer