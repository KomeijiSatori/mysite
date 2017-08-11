import re
from collections import OrderedDict

from rest_framework import serializers
from blogs.models import Blog, BlogCategory, Comment
from .pagination import BlogNumberPagination


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'publish_time',
            'last_update_time',
            'text',
            'children',
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_children(self, obj):
        return [CommentListSerializer(child).data for child in obj.get_children()]


class BlogListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name="blogs-api:blog_detail", lookup_field="pk")

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'author',
            'publish_time',
            'url',
        ]

    def get_author(self, obj):
        return obj.author.username


class BlogDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'author',
            'publish_time',
            'last_update_time',
            'text',
            'categories',
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_categories(self, obj):
        categories = obj.blogcategory_set.all()
        return [category.name for category in categories]


class BlogPostSerializer(serializers.ModelSerializer):
    categories = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Blog
        fields = [
            'title',
            'text',
            'categories',
        ]

    def validate_title(self, value):
        title = value
        if (not title) or title == "":
            raise serializers.ValidationError("Title cannot be empty!")
        return value

    def validate_text(self, value):
        text = value
        if (not text) or text == "":
            raise serializers.ValidationError("Content cannot be empty!")
        http_links = re.findall(r'\[\d+\]: http://[^\s]*', text)
        if len(http_links) > 0:
            raise serializers.ValidationError("Http link found! Only Https link is allowed! " + " ".join(http_links))
        return value

    def validate_categories(self, value):
        category_text = value
        if category_text and category_text != '':
            category = category_text.split(' ')
            if '' in category:
                raise serializers.ValidationError("Too many spaces between tags!")
            if len(category) != len(set(category)):
                raise serializers.ValidationError("Redundant tags exist!")
        return value


class BlogUpdateSerializer(serializers.ModelSerializer):
    categories = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Blog
        fields = [
            'title',
            'text',
            'categories',
        ]
        extra_kwargs = {
            'title': {'required': False},
            'text': {'required': False},
        }

    def validate_title(self, value):
        title = value
        if title and title == "":
            raise serializers.ValidationError("Title cannot be empty!")
        return value

    def validate_text(self, value):
        text = value
        if text:
            if text == "":
                raise serializers.ValidationError("Content cannot be empty!")
            http_links = re.findall(r'\[\d+\]: http://[^\s]*', text)
            if len(http_links) > 0:
                raise serializers.ValidationError("Http link found! Only Https link is allowed! " +
                                                  " ".join(http_links))
        return value

    def validate_categories(self, value):
        category_text = value
        if category_text and category_text != '':
            category = category_text.split(' ')
            if '' in category:
                raise serializers.ValidationError("Too many spaces between tags!")
            if len(category) != len(set(category)):
                raise serializers.ValidationError("Redundant tags exist!")
        return value


class BlogCommentListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'comments',
        ]

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        return [CommentListSerializer(comment).data for comment in comments.filter(parent=None)]


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]


class BlogCategoryListSerializer(serializers.ModelSerializer):
    blogs = serializers.SerializerMethodField()

    class Meta:
        model = BlogCategory
        fields = [
            'name',
            'blogs',
        ]

    def get_blogs(self, obj):
        category_blogs = obj.blog.all()
        paginator = BlogNumberPagination()
        blogs = paginator.paginate_queryset(category_blogs, self.context['request'])
        serializer = BlogListSerializer(blogs, many=True, context={'request': self.context['request']})

        res = OrderedDict([
            ('count', paginator.page.paginator.count),
            ('next', paginator.get_next_link()),
            ('previous', paginator.get_previous_link()),
            ('results', serializer.data)
        ])
        return res
