from django.urls import path
from .views import PostListView, PostDetailView, FeaturedPostsView, CategoryListView, CommentCreateView

urlpatterns = [
    path('blogs/', PostListView.as_view(), name='api-blog-list'),
    path('blogs/featured/', FeaturedPostsView.as_view(), name='api-blog-featured'),
    path('blogs/<slug:slug>/', PostDetailView.as_view(), name='api-blog-detail'),
    path('blogs/<slug:slug>/comments/', CommentCreateView.as_view(), name='api-blog-comment'),
    path('categories/', CategoryListView.as_view(), name='api-categories'),
]
