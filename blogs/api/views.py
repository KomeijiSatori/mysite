from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError

from blogs.models import Blog, Comment, BlogCategory
from blogs.service import BlogService
from .serializers import BlogListSerializer, BlogDetailSerializer, \
    BlogPostSerializer, BlogUpdateSerializer, BlogCommentListSerializer, \
    CommentPostSerializer, CommentListSerializer
from .permissions import IsOwnerOrSuperUser
from .pagination import BlogNumberPagination


class BlogListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogListSerializer
    pagination_class = BlogNumberPagination
    http_method_names = ['get']


class BlogDetailView(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    http_method_names = ['get']


class BlogUpdateView(UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogUpdateSerializer
    permission_classes = [IsOwnerOrSuperUser]
    http_method_names = ['put']

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
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def perform_create(self, serializer):
        title_str = serializer.validated_data.get('title')
        text_str = serializer.validated_data.get('text')
        category_str = serializer.validated_data.get('categories')
        user = self.request.user
        # the cleaned data will swallow space which would break markdown format
        # blog.text = form.cleaned_data.get('text')
        blog = BlogService.create_blog_from_string(user, title_str, text_str, category_str)
        serializer.validated_data['id'] = blog.id


class BlogCommentView(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCommentListSerializer
    http_method_names = ['get']


class CommentListView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    http_method_names = ['get']


class CommentCreateView(CreateAPIView):
    serializer_class = CommentPostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def perform_create(self, serializer):
        blog_id = self.kwargs.get('blog_id')
        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            blog = None
        user = self.request.user
        if blog:
            text = serializer.validated_data.get("text")
            comment = BlogService.create_comment_from_string(user, blog, text, None)
            serializer.validated_data['id'] = comment.id
        else:
            raise NotFound(detail="Blog does not exist", code=404)


class NestedCommentCreateView(CreateAPIView):
    serializer_class = CommentPostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def perform_create(self, serializer):
        comment_id = self.kwargs.get('comment_id')
        try:
            parent_comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            parent_comment = None
        user = self.request.user
        if parent_comment:
            text = serializer.validated_data.get("text")
            blog = parent_comment.blog
            comment = BlogService.create_comment_from_string(user, blog, text, parent_comment)
            serializer.validated_data['id'] = comment.id
        else:
            raise NotFound(detail="Comment does not exist", code=404)


class CommentUpdateView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentPostSerializer
    permission_classes = [IsOwnerOrSuperUser]
    http_method_names = ['put']

    def perform_update(self, serializer):
        text_str = serializer.validated_data.get('text')
        comment_id = self.get_object().id
        comment = BlogService.update_comment_from_string(comment_id, text_str)

    # override self.get_serializer method to display the right serializer.data
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


class BlogCategoryListView(ListAPIView):
    serializer_class = BlogListSerializer
    pagination_class = BlogNumberPagination
    http_method_names = ['get']
    lookup_field = "name"

    def get_queryset(self):
        name = self.kwargs.get('name')
        cate = BlogCategory.objects.filter(name=name)
        if len(cate) == 1:
            return cate[0].blog.all()
        else:
            return []


class BlogSearchView(ListAPIView):
    serializer_class = BlogListSerializer
    pagination_class = BlogNumberPagination
    http_method_names = ['get']

    def get_queryset(self):
        paras = dict(self.request.GET)
        try:
            blogs = BlogService.search_blogs(**paras)
        except Exception as e:
            raise ParseError(str(e))
        return blogs
