from django.urls import path
from .views import (
    PostListView, PostDetailView, FeaturedPostsView,
    CategoryListView, CommentCreateView,
    PostCreateView, PostUpdateView, PostDeleteView,
    StaffPostListView, CategoryCreateView,
)

urlpatterns = [
    path('blogs/', PostListView.as_view(), name='api-blog-list'),
    path('blogs/featured/', FeaturedPostsView.as_view(), name='api-blog-featured'),
    path('blogs/staff/', StaffPostListView.as_view(), name='api-blog-staff'),
    path('blogs/create/', PostCreateView.as_view(), name='api-blog-create'),
    path('blogs/<slug:slug>/', PostDetailView.as_view(), name='api-blog-detail'),
    path('blogs/<slug:slug>/update/', PostUpdateView.as_view(), name='api-blog-update'),
    path('blogs/<slug:slug>/delete/', PostDeleteView.as_view(), name='api-blog-delete'),
    path('blogs/<slug:slug>/comments/', CommentCreateView.as_view(), name='api-blog-comment'),
    path('categories/', CategoryListView.as_view(), name='api-categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='api-category-create')
]
