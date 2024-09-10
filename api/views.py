from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from api import serializers
from api.models import Tag, Post, Category


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()  # noqa
    serializer_class = serializers.TagSerializer
    search_fields = ['title']

    def get_queryset(self):
        tags = cache.get('post_tags')
        if tags is None:
            tags = Tag.objects.all()  # noqa
            serializer = self.serializer_class(tags, many=True)
            cache.set('post_tags', serializer.data)  # Store serialized data in cache
            return tags
        else:
            # Create a list of Tag objects from the cached data
            tags = [Tag(**item) for item in tags]
            # Use the Django model manager to create a queryset from the list
            return Tag.objects.filter(id__in=[tag.id for tag in tags])  # noqa

    @extend_schema(operation_id='listTag', tags=['Tag'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TagDetailAPIView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()  # noqa
    serializer_class = serializers.TagSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = cache.get(f'post_tag_{pk}')
        if obj is None:
            obj = super().get_object()
            serializer = self.serializer_class(obj)
            cache.set(f'post_tag_{pk}', serializer.data)  # Store serialized data in cache
            return obj
        else:
            obj = Tag(**obj)  # Convert cached data back to Tag object
            return obj

    @extend_schema(operation_id='retrieveTag', tags=['Tag'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TagCreateAPIView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagCreateSerializer

    @extend_schema(operation_id='createTag', tags=['Tag'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            cache.delete('post_tags')
        return response


class TagUpdateAPIView(generics.UpdateAPIView):
    queryset = Tag.objects.all()  # noqa
    serializer_class = serializers.TagUpdateSerializer

    @extend_schema(operation_id='updateTagPut', tags=['Tag'])
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a tag is updated
            cache.delete('post_tags')
            pk = kwargs.get('pk')
            cache.delete(f'post_tag_{pk}')
        return response

    @extend_schema(operation_id='updateTagPatch', tags=['Tag'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a tag is updated
            cache.delete('post_tags')
            pk = kwargs.get('pk')
            cache.delete(f'post_tag_{pk}')
        return response


class TagDeleteAPIView(generics.DestroyAPIView):
    queryset = Tag.objects.all()  # noqa
    serializer_class = serializers.TagSerializer

    @extend_schema(
        operation_id='deleteTag',
        tags=['Tag'],
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        # Invalidate the list and detail cache when a tag is deleted
        cache.delete('post_tags')
        cache.delete(f'post_tag_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()  # noqa
    serializer_class = serializers.PostListSerializer
    search_fields = ['title', 'content', 'category__title']

    @extend_schema(operation_id='listPost', tags=['Post'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()  # noqa
    serializer_class = serializers.PostDetailSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = cache.get(f'post_{pk}')
        if obj is None:
            obj = super().get_object()
            serializer = self.serializer_class(obj)
            cache.set(f'post_{pk}', serializer.data)  # Store serialized data in cache
            return obj
        else:
            obj = Post(**obj)  # Convert cached data back to Post object
            return obj

    @extend_schema(operation_id='retrievePost', tags=['Post'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()  # noqa
    serializer_class = serializers.PostCreateSerializer

    @extend_schema(operation_id='createPost', tags=['Post'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Invalidate the list cache when a new post is created
            cache.delete('posts')
        return response


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()  # noqa
    serializer_class = serializers.PostUpdateSerializer

    @extend_schema(operation_id='updatePostPut', tags=['Post'])
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a post is updated
            cache.delete('posts')
            pk = kwargs.get('pk')
            cache.delete(f'post_{pk}')
        return response

    @extend_schema(operation_id='updatePostPatch', tags=['Post'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a post is updated
            cache.delete('posts')
            pk = kwargs.get('pk')
            cache.delete(f'post_{pk}')
        return response


class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()  # noqa
    serializer_class = serializers.PostDetailSerializer

    @extend_schema(
        operation_id='deletePost',
        tags=['Post'],
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        # Invalidate the list and detail cache when a post is deleted
        cache.delete('posts')
        cache.delete(f'post_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategorySerializer
    search_fields = ['title']

    def get_queryset(self):
        categories = cache.get('post_categories')
        if categories is None:
            categories = Category.objects.all()  # noqa
            serializer = self.serializer_class(categories, many=True)
            cache.set('post_categories', serializer.data)  # Store serialized data in cache
            return categories
        else:
            # Create a list of Category objects from the cached data
            categories = [Category(**item) for item in categories]
            # Use the Django model manager to create a queryset from the list
            return Category.objects.filter(id__in=[category.id for category in categories])  # noqa

    @extend_schema(operation_id='listCategory', tags=['Category'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategorySerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = cache.get(f'post_category_{pk}')
        if obj is None:
            obj = super().get_object()
            serializer = self.serializer_class(obj)
            cache.set(f'post_category_{pk}', serializer.data)  # Store serialized data in cache
            return obj
        else:
            obj = Category(**obj)  # Convert cached data back to Category object
            return obj

    @extend_schema(operation_id='retrieveCategory', tags=['Category'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryCreateSerializer

    @extend_schema(operation_id='createCategory', tags=['Category'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Invalidate the list cache when a new category is created
            cache.delete('post_categories')
        return response


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryUpdateSerializer

    @extend_schema(operation_id='updateCategoryPut', tags=['Category'])
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a category is updated
            cache.delete('post_categories')
            pk = kwargs.get('pk')
            cache.delete(f'post_category_{pk}')
        return response

    @extend_schema(operation_id='updateCategoryPatch', tags=['Category'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a category is updated
            cache.delete('post_categories')
            pk = kwargs.get('pk')
            cache.delete(f'post_category_{pk}')
        return response


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategorySerializer

    @extend_schema(operation_id='deleteCategory', tags=['Category'])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        # Invalidate the list and detail cache when a category is deleted
        cache.delete('post_categories')
        cache.delete(f'post_category_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)