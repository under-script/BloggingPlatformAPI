from rest_framework.exceptions import ValidationError


def validate_search_term(search_term):
    if not search_term:
        return
    if len(search_term.strip()) <= 1:
        raise ValidationError("Search term must be more than one character.")