from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import markdown


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    color = models.CharField(max_length=7, default='#00f5d4', help_text='Hex color for badge')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True, max_length=350)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    excerpt = models.TextField(max_length=500, help_text='Short summary shown in cards')
    content = models.TextField(help_text='Write in Markdown')
    cover_image = models.ImageField(upload_to='blog/covers/', blank=True, null=True)
    read_time = models.PositiveIntegerField(default=5, help_text='Estimated read time in minutes')
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def content_html(self):
        """Convert markdown content to HTML."""
        return markdown.markdown(
            self.content,
            extensions=['markdown.extensions.fenced_code', 'markdown.extensions.tables',
                       'markdown.extensions.codehilite', 'markdown.extensions.toc']
        )

    def increment_views(self):
        Post.objects.filter(pk=self.pk).update(views=models.F('views') + 1)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField(max_length=1000)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.name} on "{self.post.title}"'
