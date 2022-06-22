from django.shortcuts import render
from rest_framework.generics import ListAPIView

from market.models import Character, Server
from market.serializers import CharacterSerializer, ServerSerializer


class CharacterListAPIView(ListAPIView):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()


class ServerListAPIView(ListAPIView):
    serializer_class = ServerSerializer
    queryset = Server.objects.all()


