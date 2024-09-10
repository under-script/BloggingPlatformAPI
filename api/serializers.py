from rest_framework import serializers

from api.models import Post, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        search_fields = ['title']


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        # fields = ['title']
        fields = ["id", 'title']
        read_only_fields = ["id"]


class TagUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", 'title']
        read_only_fields = ["id"]


class PostListSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.title')

    class Meta:
        model = Post
        fields = '__all__'
        search_fields = ['title']
        extra_kwargs = {
            'tags': {'required': False}, # noqa
            # Add other fields as needed
        }
        # exclude = ('tags',) # noqa


class PostDetailSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.title')
    tags = serializers.SlugRelatedField(many=True, slug_field='title', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    tags = TagCreateSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            "id", 'title', 'content', 'category', 'tags'
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        blog = Post.objects.create(**validated_data) # noqa
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            blog.tags.add(tag)
        return blog


def create_or_update_tags(tags):
    return [Tag.objects.update_or_create(pk=tag.get('id'), defaults=tag)[0].pk for tag in tags]


class PostUpdateSerializer(serializers.ModelSerializer):
    tags = TagCreateSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = [
            "id", 'title', 'content', 'category', 'tags'
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        if tags_data is not None:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(**tag_data)
                instance.tags.add(tag)
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        search_fields = ['title']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", 'title']
        read_only_fields = ["id"]


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", 'title']
        read_only_fields = ["id"]