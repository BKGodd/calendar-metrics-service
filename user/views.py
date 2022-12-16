from user.models import User
from user.serializers import UserSerializer
from user.calendar import auth_google, webhook, calc_metrics

from rest_framework import viewsets
from rest_framework.response import Response
from django.conf import settings

import os


class UserList(viewsets.ModelViewSet):
    """
    A class-based view

    Note:
        Classes are meant to group endpoints. If multiple different POSTs are made
        on one endpoint, edit urls.py to route specific methods under one class
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get(self, request, pk=None):
        """
        GET method of the endpoint

        Args:
            request (Request object): Request made to server
            pk (str): Primary key of the associated user
        """
        items = User.objects.all()
        serializer = UserSerializer(items, many=True)
        return Response(serializer.data)


    def delete(self, request, pk):
        """
        DELETE method of the endpoint

        Args:
            request (Request object): Request made to server
            pk (str): Primary key of the associated user
        """
        item = User.objects.get(id=pk)
        item.delete()
        serializer = UserSerializer(item)
        return Response(serializer.data)


    def post(self, request, pk=None):
        """
        POST method of the endpoint

        Args:
            request (Request object): Request made to server
            pk (str): Primary key of the associated user
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the valid data to postgres database
            serializer.save()
            # This is the user's first time "signing in", create the web hook
            # Use the user's ID to establish the watch channel, avoids us using
            # only one URL for all users
            destination = os.path.join(settings.CHANNEL_DESTINATION, serializer.data['id'])
            creds = auth_google()
            webhook(creds, serializer.data['id'], destination)
            return Response(serializer.data)
        return Response(serializer.errors)
    

    def post_calendar(self, request, pk):
        """
        POST method of the endpoint (for Google watch events), indicating
        a change has been made to a user's Google Calendar

        Args:
            request (Request object): Request made to server
            pk (str): Primary key of the associated user
        """
        serializer = UserSerializer(data=request.data)
        # Ensure the request is coming from Google
        if 'X-Goog-Channel-ID' in request.headers:
            # Calculate real-time basic metrics of the calendar
            creds = auth_google()
            calc_metrics(creds)

        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors)
