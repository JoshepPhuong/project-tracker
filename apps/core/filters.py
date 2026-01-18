from django import forms

from django_filters import rest_framework as filters

from .forms import TolerantDateField


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """Filter class for filtering list of number."""


class IntegerInFilter(filters.BaseInFilter, filters.NumberFilter):
    """Filter class for filtering list of integer."""

    field_class = forms.IntegerField


class ModelMultipleChoiceFilter(
    filters.BaseInFilter,
    filters.ModelChoiceFilter,
):
    """Filter class for filtering model choices."""


class MultipleChoiceFilter(filters.BaseInFilter, filters.ChoiceFilter):
    """Filter class for filtering choices."""


class TolerantDateFilter(filters.DateFilter):
    """Provide a custom DateFilter.

    If the day passed to the filter is not a valid date,
    it will return the whole queryset instead of raising errors.

    """

    field_class = TolerantDateField


class MultipleDateFilter(filters.BaseInFilter, filters.DateFilter):
    """Filter by multiple dates."""
