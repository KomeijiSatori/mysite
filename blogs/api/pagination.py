from rest_framework.pagination import PageNumberPagination
from blogs.service import BlogService


class BlogNumberPagination(PageNumberPagination):
    page_size = BlogService.item_show_per_page
    page_size_query_param = 'page_size'
    max_page_size = 20
