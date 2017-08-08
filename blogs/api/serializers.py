import re

from rest_framework import serializers
from blogs.models import Blog, BlogCategory, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = [
            'name',
        ]


class CommentSerializer(serializers.ModelSerializer):
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
        return [CommentSerializer(child).data for child in obj.get_children()]


class BlogListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'author',
            'publish_time',
        ]

    def get_author(self, obj):
        return obj.author.username


class BlogDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    blogcategory_set = CategorySerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'author',
            'publish_time',
            'last_update_time',
            'text',
            'blogcategory_set',
            'comments',
        ]

    def get_author(self, obj):
        return obj.author.username

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        return [CommentSerializer(comment).data for comment in comments.filter(parent=None)]


class BlogPostSerializer(serializers.ModelSerializer):
    categories = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Blog
        fields = [
            'title',
            'text',
            'categories',
        ]

    def validate(self, data):
        title = data.get("title")
        text = data.get("text")
        category_text = data.get("categories")

        if (not title) or title == "":
            raise serializers.ValidationError("Title cannot be empty!")

        if (not text) or text == "":
            raise serializers.ValidationError("Content cannot be empty!")
        http_links = re.findall(r'\[\d+\]: http://[^\s]*', text)
        if len(http_links) > 0:
            raise serializers.ValidationError("Http link found! Only Https link is allowed! " + " ".join(http_links))

        if category_text and category_text != '':
            category = category_text.split(' ')
            if '' in category:
                raise serializers.ValidationError("Too many spaces between tags!")
            if len(category) != len(set(category)):
                raise serializers.ValidationError("Redundant tags exist!")
        return data
