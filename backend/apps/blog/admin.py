from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['name', 'email', 'content', 'created_at']
    fields = ['name', 'email', 'content', 'is_approved', 'created_at']
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'views', 'published_at']
    list_filter = ['status', 'category', 'is_featured']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    readonly_fields = ['views', 'created_at', 'updated_at']
    inlines = [CommentInline]
    fieldsets = (
        ('Content', {'fields': ('title', 'slug', 'category', 'excerpt', 'content', 'cover_image')}),
        ('Settings', {'fields': ('status', 'is_featured', 'read_time')}),
        ('Stats', {'fields': ('views', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    actions = ['publish_posts', 'unpublish_posts']

    def publish_posts(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, f'{queryset.count()} posts published.')
    publish_posts.short_description = 'Publish selected posts'

    def unpublish_posts(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, f'{queryset.count()} posts unpublished.')
    unpublish_posts.short_description = 'Unpublish selected posts'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved']
    list_editable = ['is_approved']
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
