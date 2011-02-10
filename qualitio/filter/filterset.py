import django_filters

from qualitio.filter.filters import RelatedObjectFilter


class ModelFilterSet(django_filters.FilterSet):
    """
    Base class for filterset's. It change every
    CharFilter.lookup_type to 'icontains'.

    It also adds filters for reverse foreign key relations dynamically.
    """

   def __init__(self, *args, **kwargs):
       super(django_filters.FilterSet, self).__init__(*args, **kwargs)
       for f in self.filters.values():
           if issubclass(f.__class__, (django_filters.CharFilter,)):
               f.lookup_type = 'icontains'

       this_model = self._meta.model
       for ro in this_model._meta.get_all_related_objects():
           if ro.field.name is not "parent":
               filter = RelatedObjectFilter(ro, name=ro.var_name, label=("%s exists" % ro.var_name).capitalize())
               self.filters[ro.var_name] = filter
