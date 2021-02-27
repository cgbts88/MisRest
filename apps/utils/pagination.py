from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from math import ceil


class CommonPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        filters = "&".join([item[0] + '=' + item[1] for item in self.request.GET.items() if item[0] != 'page'])
        around_count = 1
        left_has_more = False
        right_has_more = False
        total_page = ceil(self.page.paginator.count/self.page_size)
        cur_page = self.page.number
        left_page = []
        if cur_page <= around_count + 1:
            left_page_range = range(1, cur_page)
        else:
            left_has_more = True
            left_page_range = range(cur_page - around_count, cur_page)
        for page in left_page_range:
            left_page.append(page)

        right_page = []
        if cur_page >= total_page - around_count - 1:
            right_page_range = range(cur_page + 1, total_page + 1)
        else:
            right_has_more = True
            right_page_range = range(cur_page + 1, cur_page + 3)
        for page in right_page_range:
            right_page.append(page)

        pages = []
        if left_has_more:
            pages.append(1)
            pages.append('...')
        print('pages:', pages)

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
