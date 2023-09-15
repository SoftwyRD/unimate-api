from __future__ import annotations

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

LinkHeader = str


class HeaderPagination(PageNumberPagination):
    """Header based pagination

    Pagination metadata are specified in response's headers.
    Information about pagination is provided in the Link header.

    Headers:
    --------
    X-Page-Count: Total page count
    X-Current-Page: Current page number
    X-Page-Size: Item count in the current page
    X-Total: Total number of item included if `include_count` is `True`

    Link: previous, next, first & last links.
          See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Link

    Parameters
    ----------
    include_count: Include result set count in `X-Total` header.
    """

    page_size_query_param = "page_size"
    include_count = True
    page_size = 25
    max_page_size = 100

    def get_links(self) -> list[LinkHeader]:
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        first_url = self.get_first_link()
        last_url = self.get_last_link()
        links = []
        for url, label in (
            (first_url, "first"),
            (previous_url, "prev"),
            (next_url, "next"),
            (last_url, "last"),
        ):
            if url is not None:
                links.append(f'<{url}>; rel="{label}"')

        return links

    def get_paginated_response(self, data) -> Response:
        links = self.get_links()

        page_count = self.page.paginator.num_pages

        headers = {
            "X-Page-Count": page_count,
            "X-Page-Size": self.page_size,
            "X-Current-Page": self.page.number,
        }

        if self.include_count:
            headers.update({"X-Total": self.page.paginator.count})

        if links:
            headers.update({"Link": ", ".join(links)})

        return Response(data, headers=headers)

    def get_first_link(self) -> str:
        if not self.page.has_previous():
            return None
        else:
            url = self.request.build_absolute_uri()
            return remove_query_param(url, self.page_query_param)

    def get_last_link(self) -> str:
        if not self.page.has_next():
            return None
        else:
            url = self.request.build_absolute_uri()
            return replace_query_param(
                url,
                self.page_query_param,
                self.page.paginator.num_pages,
            )

    def get_paginated_response_schema(self, schema: dict) -> dict:
        return schema
