from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response

from blogs.models import Blog
from blogs.service import BlogService
from .serializers import BlogListSerializer, BlogDetailSerializer, BlogPostSerializer


class BlogListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    # lookup_field = 'id'


class BlogDetailView(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    # lookup_field = 'id'


class BlogUpdateView(UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogPostSerializer
    # lookup_field = 'id'

    # override the default update method to avoid get_serializer with 'instance' as parameter(which will cause 500)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        title_str = serializer.validated_data.get('title')
        text_str = serializer.validated_data.get('text')
        category_str = serializer.validated_data.get('categories')
        blog_id = self.get_object().id
        blog = BlogService.update_blog_from_string(blog_id, title_str, text_str, category_str)


class BlogCreateView(CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogPostSerializer

    def perform_create(self, serializer):
        title_str = serializer.validated_data.get('title')
        text_str = serializer.validated_data.get('text')
        category_str = serializer.validated_data.get('categories')
        user = self.request.user
        # the cleaned data will swallow space which would break markdown format
        # blog.text = form.cleaned_data.get('text')
        blog = BlogService.create_blog_from_string(user, title_str, text_str, category_str)

