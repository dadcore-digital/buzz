from rest_framework.pagination import LimitOffsetPagination

class StandardResultsSetPagination(LimitOffsetPagination):
    page_size_query_param = 'page_size'
    max_page_size = 1000
    default_limit = 10
