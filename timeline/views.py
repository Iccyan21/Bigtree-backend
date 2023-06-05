from django.shortcuts import render
from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
# Create your views here.

#投稿機能
class SendPostView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    
#投稿一覧
class GetPostListView(views.APIView):
    def get(self, request, *args, **kwargs):
        post_list = Post.objects.all()
        serializer = PostSerializer(instance=post_list, many=True)
        return Response(serializer.data)

