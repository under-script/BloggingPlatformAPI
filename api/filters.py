from re import search

from rest_framework.filters import BaseFilterBackend
from django.db.models import Q

from BloggingPlatformAPI import settings
from api.validators import validate_search_term


class CustomSearchFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_term = request.query_params.get(settings.REST_FRAMEWORK.get('SEARCH_PARAM'), None)

        # Validate search term
        validate_search_term(search_term)

        if search_term:
            return queryset.filter(
                Q(title__icontains=search_term) |
                Q(content__icontains=search_term) |
                Q(category__name__icontains=search_term) |
                Q(tags__name__icontains=search_term)
            ).distinct()
        return queryset

