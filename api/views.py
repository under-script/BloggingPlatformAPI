from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
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

    @extend_schema(
        request=CategorySerializer,
        examples=[
            OpenApiExample(
                'Example Category Creation Request',
                value={
                    'name': 'Technology'
                },
                request_only=True,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=CategorySerializer,
                examples=[
                    OpenApiExample(
                        'Example Category Creation Response',
                        value={
                            'id': 1,
                            'name': 'Technology'
                        },
                    ),
                ]
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='A list of categories',
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Example Category List Response',
                        value=[
                            {'id': 1, 'name': 'Technology'},
                            {'id': 2, 'name': 'Science'}
                        ],
                    ),
                ]
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @extend_schema(
        request=TagSerializer,
        examples=[
            OpenApiExample(
                'Example Tag Creation Request',
                value={
                    'name': 'Tech'
                },
                request_only=True,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=TagSerializer,
                examples=[
                    OpenApiExample(
                        'Example Tag Creation Response',
                        value={
                            'id': 1,
                            'name': 'Tech'
                        },
                    ),
                ]
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description='A list of tags',
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Example Tag List Response',
                        value=[
                            {'id': 1, 'name': 'Tech'},
                            {'id': 2, 'name': 'Programming'}
                        ],
                    ),
                ]
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)