from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from math import ceil


class CommonPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        page_num = ceil(self.page.paginator.count/self.page_size)
        cur_page = self.page.number
        if cur_page - 5 < 1:
            page_range = range(1, 10)
        elif cur_page + 5 > page_num:
            page_range = range(cur_page-5, page_num+1)
        else:
            page_range = range(cur_page-5, cur_page+5)
        return Response(OrderedDict([
            ('current', cur_page),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_range', page_range),
            ('results', data)
        ]))
