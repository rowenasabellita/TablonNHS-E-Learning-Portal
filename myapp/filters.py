import django_filters
from .models import UserProfile

class FilterSearch(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = '__all__'
