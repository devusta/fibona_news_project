from django.contrib import admin
from news.models import News, Category, Contact, Comment


# Modelni admin panelga registratsiya qilishning 1-usuli
@admin.register(News) # 1-usul dekoratsiya bilan
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish_time', 'status', 'category')
    list_filter = ('status', 'created_time', 'publish_time', 'category')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ('title', 'slug', 'body')
    ordering = ('publish_time', 'status')


# Modelni admin panelga registratsiya qilishning 2-usuli
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)


admin.site.register(Category, CategoryAdmin) # 2-usul oddiy funksiya bilan
admin.site.register(Contact)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'author', 'created_time', 'is_active')
    list_filter = ('is_active', 'created_time',)
    search_fields = ('author', 'body')
    actions = ['disable_comments', 'enable_comments']

    def disable_comments(self, queryset):
        queryset.update(is_active=False)

    def enable_comments(self, queryset):
        queryset.update(is_active=True)


admin.site.register(Comment, CommentAdmin)

