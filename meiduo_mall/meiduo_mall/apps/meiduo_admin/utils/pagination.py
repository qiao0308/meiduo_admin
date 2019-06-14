from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MeiduoPagination(PageNumberPagination):
    # 默认页大小
    page_size = 1
    # 最大页大小
    max_page_size = 10
    # 指定页大小的查询参数键，使用如：***?pagesize=3
    page_size_query_param = 'pagesize'

    # 自定义响应体
    def get_paginated_response(self, data):
        # self.page===>Page
        # self.page.paginator==>Paginator
        return Response({
            "counts": self.page.paginator.count,
            "lists": data,
            "page": self.page.number,
            "pages": self.page.paginator.num_pages,
            "pagesize": self.page.paginator.per_page
        })