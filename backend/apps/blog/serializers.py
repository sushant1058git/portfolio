from rest_framework import serializers
from .models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'color', 'post_count']

    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'content', 'created_at']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Comment must be at least 10 characters.')
        return value


class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    published_date = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'category', 'excerpt',
            'cover_image', 'read_time', 'views', 'is_featured',
            'published_date', 'published_at'
        ]

    def get_published_date(self, obj):
        if obj.published_at:
            return obj.published_at.strftime('%b %Y').upper()
        return ''


class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source='approved_comments')
    content_html = serializers.ReadOnlyField()
    published_date = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'category', 'excerpt', 'content',
            'content_html', 'cover_image', 'read_time', 'views', 'is_featured',
            'published_date', 'published_at', 'comments', 'comment_count'
        ]

    def get_published_date(self, obj):
        if obj.published_at:
            return obj.published_at.strftime('%b %d, %Y')
        return ''

    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
