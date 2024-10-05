from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.response import Response

from BloggingPlatformAPI import settings
from api.filters import CustomSearchFilter
from api.models import Post, Category, Tag
from api.serializers import PostSerializer, CategorySerializer, TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [CustomSearchFilter]

    @extend_schema(
        parameters=[
            OpenApiParameter(name=settings.REST_FRAMEWORK.get('SEARCH_PARAM'), type=str, description='Search term for posts')
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer