from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q

from .models import Blog, BlogCategory, Comment


class BlogService(object):
    item_show_per_page = 10
    item_display_page = 7  # should be odd number

    @classmethod
    def _getPageList(cls, cur_page, page_count):
        cur_page = int(cur_page)

        if page_count <= cls.item_display_page:
            left = 1
            right = page_count
        else:
            left = int(cur_page - ((cls.item_display_page - 1) / 2 - 1))
            right = int(cur_page + ((cls.item_display_page - 1) / 2 - 1))
            if left < 2:
                right += 2 - left
                left = 2
            elif right > page_count - 1:
                left -= right - page_count + 1
                right = page_count - 1

        if left == 1:
            res = [x for x in range(left, 1 + right)]
        elif left == 2:
            res = [1] + [x for x in range(left, right + 1)]
        else:
            res = [1, "..."] + [x for x in range(left, right + 1)]
        if right <= page_count - 2:
            res += ['...', page_count]
        elif right == page_count - 1:
            res += [page_count]
        return res

    @classmethod
    def get_paginated_items(cls, item_list, current_page):
        """
        Get paginated items with page list.
        :param item_list: type: array, array that contains all items, maybe Blog or Comments
        :param current_page: type: str or int, the current page number
        :return: [items, page_list], items: array, page_list: array
        """
        paginator = Paginator(item_list, cls.item_show_per_page)

        try:
            items = paginator.page(current_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            current_page = 1
            items = paginator.page(current_page)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            current_page = paginator.num_pages
            items = paginator.page(current_page)

        page_list = cls._getPageList(current_page, paginator.num_pages)

        for item in items:
            if item.publish_time:
                item.publish_time = timezone.localtime(item.publish_time)
            if item.last_update_time:
                item.last_update_time = timezone.localtime(item.last_update_time)
        return items, page_list

    @classmethod
    def create_blog_from_string(cls, user, title_str, text_str, category_str):
        """
        Create blog from string.
        :param user: type: User, the author of the blog
        :param title_str: type: str, the new title of the blog
        :param text_str: type: str, the new content of the blog
        :param category_str: type: str, the new categories of the blog
        :return: blog: type: Blog, the created blog
        """
        categories = []
        if category_str:
            categories_str = category_str.split(' ')
            categories = list(filter(None, categories_str))

        blog = Blog()
        blog.title = title_str
        blog.author = user
        blog.text = text_str
        blog.save()

        for category in categories:
            res = BlogCategory.objects.filter(name=category)
            if res.count() == 0:
                blog_category = BlogCategory()
                blog_category.name = category
                blog_category.save()
            else:
                blog_category = res[0]
            blog_category.blog.add(blog)
        return blog

    @classmethod
    def update_blog_from_string(cls, blog_id, title_str, text_str, category_str):
        """
        Update blog from string.
        :param blog_id: type: num, the id of the blog
        :param title_str: type: str, the new title of the blog
        :param text_str: type: str, the new content of the blog
        :param category_str: type: str, the new categories of the blog
        :return: blog: type: Blog, the updated blog
        """
        categories = []
        if category_str is not None:
            categories_str = category_str.split(' ')
            categories = list(filter(None, categories_str))

        blog = Blog.objects.get(id=blog_id)
        if title_str:
            blog.title = title_str
        if text_str:
            blog.text = text_str
        blog.last_update_time = timezone.now()
        blog.save()

        former_categories = blog.blogcategory_set.all()
        for former_category in former_categories:
            # if old category is removed
            if former_category.name not in categories:
                former_category.blog.remove(blog)
                # if the category has no associated blogs
                if former_category.blog.count() == 0:
                    former_category.delete()

        for category in categories:
            if category not in former_categories:
                res = BlogCategory.objects.filter(name=category)
                if res.count() == 0:
                    blog_category = BlogCategory()
                    blog_category.name = category
                    blog_category.save()
                else:
                    blog_category = res[0]
                # add new related categories
                blog_category.blog.add(blog)
        return blog

    @classmethod
    def update_comment_from_string(cls, comment_id, comment_str):
        """
        Update comments from string.
        :param comment_id: type: num, the id of the comment
        :param comment_str: type: str, the new content of the comment
        :return: comment: type: Comment, the updated comment
        """
        comment = Comment.objects.get(id=comment_id)
        comment.text = comment_str
        comment.last_update_time = timezone.now()
        comment.save()

    @classmethod
    def create_comment_from_string(cls, user, blog, comment_str, parent=None):
        """
        Create comment from string.
        :param user: type: User, the author of the comment
        :param blog: type: Blog, the blog which comment belongs to
        :param comment_str: type: str, the new content of the comment
        :param parent: type: Comment, the parent of the comment
        :return: comment: type: Comment, the created Comment
        """
        comment = Comment()
        comment.author = user
        comment.blog = blog
        comment.parent = parent
        comment.text = comment_str
        comment.save()
        return comment

    @classmethod
    def search_blogs(cls, *args, **kwargs):
        """
        Get search blog list.
        :param args: leave for None
        :param kwargs: dict of keys in ["search", "title", "text", "author", "category",
        "publish_from_date", "publish_to_date", "update_from_date", "update_to_date"]
        example: {'search': ['test'], 'title': [''], 'update_from_date': ['2017-8-8'], "update_to_date": ['2017-8-9']}
        :return: [blogs], blogs: array
        """
        search = kwargs.get("search")
        optional_fields = ["title", "text", "author", "category"]
        time_fields = ["publish_from_date", "publish_to_date", "update_from_date", "update_to_date"]
        allowed_kwarg_fields = optional_fields + time_fields + ['search', 'page', 'page_size']
        res = dict()

        invalid_keys = [key for key in kwargs.keys() if key not in allowed_kwarg_fields]
        if len(invalid_keys) > 0:
            raise Exception("Invalid field: {}".format(invalid_keys))

        if search is None:
            raise Exception("Search field is None")
        if len(search) > 1:
            raise Exception("Multiple search fields")
        search = search[0].strip()
        if search == "":
            raise Exception("Empty search fields")

        for field_name in optional_fields:
            field = kwargs.get(field_name)
            if field:
                if len(field) > 1:
                    raise Exception("Multiple {} fields".format(field_name))
                else:
                    res[field_name] = True
            else:
                res[field_name] = False

        for field_name in time_fields:
            field = kwargs.get(field_name)
            if field:
                if len(field) > 1:
                    raise Exception("Multiple {} fields".format(field_name))
                else:
                    res[field_name] = datetime.strptime(field[0], "%Y-%m-%d")
            else:
                res[field_name] = None

        # then select blogs by the time
        q = Q()
        if res['title']:
            q |= Q(title__icontains=search)
        if res['text']:
            q |= Q(text__icontains=search)
        if res['author']:
            q |= Q(author__username__icontains=search)
        if res['category']:
            q |= Q(blogcategory__name__icontains=search)

        # if no optional field, default to search all these fields
        if len(q) == 0:
            q = Q(title__icontains=search) | Q(text__icontains=search) | Q(author__username__icontains=search) \
                | Q(blogcategory__name__icontains=search)

        if res['publish_from_date']:
            q &= Q(publish_time__gte=res['publish_from_date'])
        if res['publish_to_date']:
            q &= Q(publish_time__lt=res['publish_to_date'])
        if res['update_from_date']:
            q &= Q(last_update_time__gte=res['update_from_date'])
        if res['update_to_date']:
            q &= Q(last_update_time__lt=res['update_to_date'])

        return Blog.objects.filter(q).distinct()
