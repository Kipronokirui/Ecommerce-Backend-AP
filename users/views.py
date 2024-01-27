from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (User, UserSerializer)

# Create your views here.
class GetUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        # print(f"User: {user_id}")
        user_profile = User.objects.get(id=user_id)
        serializer = UserSerializer(user_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
