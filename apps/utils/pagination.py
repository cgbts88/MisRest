from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from math import ceil


class CommonPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        filters = "&".join([item[0] + '=' + item[1] for item in self.request.GET.items() if item[0] != 'page'])
        around_count = 2
        left_has_more = False
        right_has_more = False
        total_page = ceil(self.page.paginator.count/self.page_size)
        cur_page = self.page.number
        if cur_page <= around_count + 2:
            left_page = range(1, cur_page)
        else:
            left_has_more = True
            left_page = range(cur_page - around_count, cur_page)
        if cur_page >= total_page - around_count - 1:
            right_page = range(cur_page + 1, total_page + 1)
        else:
            right_has_more = True
            right_page = range(cur_page + 1, cur_page + 3)

        return Response(OrderedDict([
            ('q', filters),
            ('left_pages', left_page),
            ('right_pages', right_page),
            ('cur_page', cur_page),
            ('left_has_more', left_has_more),
            ('right_has_more', right_has_more),
            ('total_page', total_page),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
