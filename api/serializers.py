from rest_framework import serializers
from .models import Post, Category, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('view').action == 'list':
            self.fields['tags'] = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
        elif self.context.get('view').action == 'retrieve':
            self.fields['tags'] = TagSerializer(many=True)

    def get_tags(self, obj):
        # This method is needed because `SerializerMethodField` is used
        if self.context.get('view').action == 'list':
            return [tag.id for tag in obj.tags.all()]
        elif self.context.get('view').action == 'retrieve':
            return TagSerializer(obj.tags.all(), many=True).data