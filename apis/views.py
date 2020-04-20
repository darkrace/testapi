from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, HttpResponseRedirect
import json
import requests
from rest_framework.viewsets import GenericViewSet
import random
from rest_framework.response import Response
from rest_framework import serializers, viewsets,mixins, permissions, status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.access_token import AccessToken
from utils.ms365_sele import MS365
# Create your views here.
from apis.models import WebexAuth
from apis.serializers import WebexAuthSerializer, UserSerializer


class IndexView(View):
    template_name = 'test.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/home")
        else:
            return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name", None)
        password = request.POST.get("password", None)
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            return render(request, self.template_name)

class MS365View(View):
    template_name = 'ms365.html'
    ms = ""
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={"flag":False})

    def post(self, request, *args, **kwargs):
        flag = request.POST.get('flag')
        if flag == "F":
            self.ms = MS365()
            phone = request.POST.get('phone')
            result = self.ms.ms_create(phone)
            return render(request, self.template_name, context=result)

        else:
            code = request.POST.get('code')
            result = self.ms.phone_verify(code)
            return render(request, "result.html", context=result)


class HomeView(View):
    template_name = 'api.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(request, self.template_name)

        else:
            return redirect("/")


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

class WebexViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = WebexAuthSerializer
    queryset = WebexAuth.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = WebexAuthSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = WebexAuthSerializer(self.queryset, many=True)
        em = request.data.get('name', None)
        pwd = request.data.get('password', None)
        ac = AccessToken()
        result = ac.token(em, pwd)
        return Response(result, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer