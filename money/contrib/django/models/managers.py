from django.db import models
from fields import currency_field_name

__all__ = ('MoneyManager',)


class MoneyManager(models.Manager):
    
    def _update_params(self, kwargs):
        from django.db.models.query import LOOKUP_SEPARATOR
        from money import Money
        to_append = {}
        for name, value in kwargs.items():
            if isinstance(value, Money):
                path = name.split(LOOKUP_SEPARATOR)
                if len(path) > 1:
                    field_name = currency_field_name(path[0])
                else:
                    field_name = currency_field_name(name)
                to_append[field_name] = value.currency
        kwargs.update(to_append)
        return kwargs
        
    def dates(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().dates(*args, **kwargs)

    def distinct(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().distinct(*args, **kwargs)

    def extra(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().extra(*args, **kwargs)

    def get(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().get(*args, **kwargs)

    def get_or_create(self, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().get_or_create(**kwargs)
        
    def create(self, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().create(**kwargs)

    def filter(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().filter(*args, **kwargs)

    def complex_filter(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().complex_filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().exclude(*args, **kwargs)

    def in_bulk(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().in_bulk(*args, **kwargs)

    def iterator(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().iterator(*args, **kwargs)

    def latest(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().latest(*args, **kwargs)

    def order_by(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().order_by(*args, **kwargs)

    def select_related(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().select_related(*args, **kwargs)

    def values(self, *args, **kwargs):
        kwargs = self._update_params(kwargs)
        return self.get_query_set().values(*args, **kwargs)