from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from job.permissions import IsOwnerOrReadOnly
from job.serializers import JobSerializer
from job.models import Job
from job.serializers import UserSerializer

# Create your views here.
class ListCreateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def get(self,request):
        qs=Job.objects.all()
        serializer_instance=JobSerializer(qs,many=True)
        return Response(serializer_instance.data,status=status.HTTP_200_OK)


    def post(self,request):
        serializer_instance=JobSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(posted_by=request.user)
            return Response(serializer_instance.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)


class ListUpdateDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def get(self,request,id):
        j=get_object_or_404(Job,id=id)
        serializer_instance=JobSerializer(j)
        return Response(serializer_instance.data,status=status.HTTP_200_OK)

    def put(self,request,id):
        j=get_object_or_404(Job,id=id)
        self.check_object_permissions(request, j)
        serializer_instance=JobSerializer(j,data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,id):
        j=get_object_or_404(Job,id=id)
        self.check_object_permissions(request, j)
        j.delete()
        return Response({'message':'Deleted Successfully'})


class RegisterView(APIView):
    def post(self,request):
        serializer_instance=UserSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)