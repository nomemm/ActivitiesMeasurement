import os

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from activities.models import Activity
from activities.serializers import ActivitySerializer, UserSerializer


class DownloadList(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, path=None, format=None):
        if not path:
            return render(
                request,
                'activities/installer.html'
            )
        else:
            file_path = os.path.join('downloadables/', path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/octet-stream")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            else:
                return Http404()


class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = User
    serializer_class = UserSerializer


class ActivityList(APIView):
    """
    List all activity list or create.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    page_size = 20

    def get(self, request, format=None):
        activities = Activity.objects.filter(user=request.user.id)
        paginator = Paginator(activities, self.page_size)
        page = request.GET.get('page')
        try:
            res = paginator.page(page)
        except PageNotAnInteger:
            res = paginator.page(1)
        except EmptyPage:
            res = paginator.page(paginator.num_pages)

        serializer = ActivitySerializer(res, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        noErrors = True
        serializers = []
        brokenSerializers = []
        for data in request.data['activities']:
            data['user'] = request.user.id
            serializer = ActivitySerializer(data=data)
            noErrors = noErrors and serializer.is_valid()
            if serializer.is_valid():
                serializer.save()
                serializers.append(serializer.data)
            else:
                brokenSerializers.append(serializer)
        if noErrors:
            return Response(
                {'activities': serializers},
                status=status.HTTP_201_CREATED
            )
        else:
            print("Error when inserting new data accured with this tuples:" +
                  repr(brokenSerializers)
                  )
            return Response(
                {'activities': serializer},
                status=status.HTTP_400_BAD_REQUEST
            )


class ActivityDetail(APIView):
    """
    Retrieve, update or delete an activity.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(request, pk):
        try:
            return Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        activity = self.get_object(pk)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        activity = self.get_object(pk)
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        activity = self.get_object(pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
