from rest_framework.pagination import (
    PageNumberPagination as BasePageNumberPagination,
)


class PageNumberPagination(BasePageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        next = self.get_next_link()
        previous = self.get_previous_link()

        return {
            "count": count,
            "next": next,
            "previous": previous,
            "results": data,
        }
