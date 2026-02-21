from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category, Post, Comment
from .serializers import (
    CategorySerializer, PostListSerializer,
    PostDetailSerializer, CommentCreateSerializer
)


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.filter(status='published').select_related('category')

        # Filter by category
        category_slug = request.query_params.get('category')
        if category_slug:
            posts = posts.filter(category__slug=category_slug)

        # Search
        search = request.query_params.get('search')
        if search:
            posts = posts.filter(title__icontains=search) | posts.filter(excerpt__icontains=search)

        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 6))
        total = posts.count()
        start = (page - 1) * page_size
        end = start + page_size

        serializer = PostListSerializer(posts[start:end], many=True, context={'request': request})
        return Response({
            'results': serializer.data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })


class PostDetailView(APIView):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug, status='published')
        post.increment_views()
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)


class FeaturedPostsView(APIView):
    def get(self, request):
        posts = Post.objects.filter(status='published', is_featured=True).select_related('category')[:3]
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CommentCreateView(APIView):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, status='published')
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(
                {'message': 'Comment submitted! It will appear after approval.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostApprovedCommentsProperty:
    """Monkey-patch to add approved_comments to Post queryset."""
    pass


# Patch Post model to support approved_comments in serializer
from apps.blog.models import Post as PostModel

@property
def approved_comments(self):
    return self.comments.filter(is_approved=True)

PostModel.approved_comments = approved_comments
