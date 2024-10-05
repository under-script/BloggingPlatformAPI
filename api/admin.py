from django.contrib import admin

from api.models import Post, Tag, Category


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    list_per_page = 10

    class Meta:
        abstract = True


class PostAdmin(BaseAdmin):
    list_display = [f.name for f in Post._meta.fields] + ["tags_list"]

    def tags_list(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    tags_list.short_description = 'Tags'


class TagAdmin(BaseAdmin):
    list_display = [f.name for f in Tag._meta.fields]


class CategoryAdmin(BaseAdmin):
    list_display = [f.name for f in Category._meta.fields]


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
