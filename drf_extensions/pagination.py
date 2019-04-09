from rest_framework.pagination import PageNumberPagination as _PageNumberPagination, \
    LimitOffsetPagination as _LimitOffsetPagination


class PageNumberPagination(_PageNumberPagination):
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        response = super(PageNumberPagination, self).get_paginated_response(data)
        response.data.update({
            "num_pages": self.page.paginator.num_pages,
            "page_size": self.get_page_size(self.request),
            "has_next": self.page.has_next()
        })
        return response


class LimitOffsetPagination(_LimitOffsetPagination):

    def get_paginated_response(self, data):
        response = super(LimitOffsetPagination, self).get_paginated_response(data)
        response.data.update({
            "page_size": self.get_limit(self.request)
        })
        return response
