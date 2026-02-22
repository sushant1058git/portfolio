from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils import timezone
from .models import Category, Post, Comment
from .serializers import (
    CategorySerializer, PostListSerializer,
    PostDetailSerializer, CommentCreateSerializer
)


def is_staff(request):
    return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.filter(status='published').select_related('category')
        category_slug = request.query_params.get('category')
        if category_slug:
            posts = posts.filter(category__slug=category_slug)
        search = request.query_params.get('search')
        if search:
            posts = posts.filter(title__icontains=search) | posts.filter(excerpt__icontains=search)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 6))
        total = posts.count()
        start = (page - 1) * page_size
        end = start + page_size
        serializer = PostListSerializer(posts[start:end], many=True, context={'request': request})
        return Response({'results': serializer.data, 'total': total, 'page': page, 'page_size': page_size, 'total_pages': (total + page_size - 1) // page_size})


class PostDetailView(APIView):
    def get(self, request, slug):
        if is_staff(request):
            post = get_object_or_404(Post, slug=slug)
        else:
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
            return Response({'message': 'Comment submitted!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        if not is_staff(request):
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        if not title or not content:
            return Response({'error': 'Title and content are required.'}, status=status.HTTP_400_BAD_REQUEST)
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        post = Post(
            title=title, slug=slug, content=content,
            excerpt=data.get('excerpt', '').strip() or content[:200],
            status=data.get('status', 'draft'),
            is_featured=data.get('is_featured') in [True, 'true', 'True', '1', 1],
            read_time=int(data.get('read_time', 5)),
        )
        if data.get('category'):
            try:
                post.category = Category.objects.get(id=data['category'])
            except Category.DoesNotExist:
                pass
        if post.status == 'published':
            post.published_at = timezone.now()
        if 'cover_image' in request.FILES:
            post.cover_image = request.FILES['cover_image']
        post.save()
        return Response(PostDetailSerializer(post, context={'request': request}).data, status=status.HTTP_201_CREATED)


class PostUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def put(self, request, slug):
        if not is_staff(request):
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        post = get_object_or_404(Post, slug=slug)
        data = request.data
        if 'title' in data: post.title = data['title'].strip()
        if 'content' in data: post.content = data['content'].strip()
        if 'excerpt' in data: post.excerpt = data['excerpt'].strip()
        if 'read_time' in data: post.read_time = int(data['read_time'])
        if 'is_featured' in data: post.is_featured = data['is_featured'] in [True, 'true', 'True', '1', 1]
        if 'status' in data:
            if data['status'] == 'published' and post.status != 'published':
                post.published_at = timezone.now()
            post.status = data['status']
        if data.get('category'):
            try:
                post.category = Category.objects.get(id=data['category'])
            except Category.DoesNotExist:
                pass
        if 'cover_image' in request.FILES:
            post.cover_image = request.FILES['cover_image']
        post.save()
        return Response(PostDetailSerializer(post, context={'request': request}).data)


class PostDeleteView(APIView):
    def delete(self, request, slug):
        if not is_staff(request):
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)


class StaffPostListView(APIView):
    def get(self, request):
        if not is_staff(request):
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        posts = Post.objects.select_related('category').order_by('-created_at')
        serializer = PostListSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryCreateView(APIView):
    def post(self, request):
        if not is_staff(request):
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        name = request.data.get('name', '').strip()
        color = request.data.get('color', '#00f5d4')
        if not name:
            return Response({'error': 'Name required.'}, status=status.HTTP_400_BAD_REQUEST)
        cat, created = Category.objects.get_or_create(name=name, defaults={'color': color})
        return Response(CategorySerializer(cat).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


from apps.blog.models import Post as PostModel

@property
def approved_comments(self):
    return self.comments.filter(is_approved=True)

PostModel.approved_comments = approved_comments
