from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.models import User
from rest_framework import status
from . import serializers

from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(["POST"])
def login(req):
    user = get_object_or_404(User, username=req.data["username"])
    if not user.check_password(req.data["password"]):
        return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = serializers.UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(["POST"])
def signup(req):
    serializer = serializers.UserSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=req.data["username"])
        user.set_password(serializer.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUser(req):
    serializer = serializers.UserSerializer(instance=req.user)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)
