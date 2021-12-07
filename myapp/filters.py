import django_filters

from .models import UserProfile

class RecordFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = ['gradelevel', 'section']