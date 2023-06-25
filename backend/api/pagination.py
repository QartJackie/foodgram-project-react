from rest_framework.pagination import PageNumberPagination


class LimitOffsetPagination(PageNumberPagination):
    """Настройка размера выдачи пагинации."""

    page_size = 6
