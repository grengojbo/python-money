from django.db import models
from django.utils.encoding import smart_unicode
from money.contrib.django import forms
from money import Money 

__all__ = ('MoneyField', 'currency_field_name', 'NotSupportedLookup')

currency_field_name = lambda name: "%s_currency" % name


SUPPORTED_LOOKUPS = ('exact', 'lt', 'gt', 'lte', 'gte')

class NotSupportedLookup(Exception):
    def __init__(self, lookup):
        self.lookup = lookup
    def __str__(self):
        return "Lookup '%s' is not supported for MoneyField" % self.lookup

class MoneyFieldProxy(object):
    def __init__(self, field):
        self.field = field
        self.currency_field_name = currency_field_name(self.field.name)
        
    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        return Money(obj.__dict__[self.field.name], obj.__dict__[self.currency_field_name])
    
    def __set__(self, obj, value):
        if isinstance(value, Money):
            obj.__dict__[self.field.name] = value.amount  
            setattr(obj, self.currency_field_name, smart_unicode(value.currency))
        else:
            obj.__dict__[self.field.name] = self.field.to_python(value) 


class MoneyField(models.DecimalField):
    
    def __init__(self, verbose_name=None, name=None, 
                 max_digits=None, decimal_places=None,
                 default=None, default_currency=None, **kwargs):
        if isinstance(default, Money):
            self.default_currency = default.currency
        self.default_currency = default_currency
        super(MoneyField, self).__init__(verbose_name, name, max_digits, decimal_places, default=default, **kwargs)
    
    def get_internal_type(self): 
         return "DecimalField"
     
    def contribute_to_class(self, cls, name):
        c_field_name = currency_field_name(name)
        c_field = models.CharField(max_length=3, default=self.default_currency, editable=False)
        c_field.creation_counter = self.creation_counter
        cls.add_to_class(c_field_name, c_field)
        
        super(MoneyField, self).contribute_to_class(cls, name)
        
        setattr(cls, self.name, MoneyFieldProxy(self))
        
    def get_db_prep_save(self, value):
        if isinstance(value, Money):
            value = value.amount  
        return super(MoneyField, self).get_db_prep_save(value)
    
    def get_db_prep_lookup(self, lookup_type, value):
        if not lookup_type in SUPPORTED_LOOKUPS: 
            raise NotSupportedLookup(lookup_type)
        value = self.get_db_prep_save(value)
        return super(MoneyField, self).get_db_prep_lookup(lookup_type, value)
    
    def get_default(self):
        if isinstance(self.default, Money):
            return self.default
        else:
            return super(MoneyField, self).get_default()
    
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.MoneyField}
        defaults.update(kwargs)
        return super(MoneyField, self).formfield(**defaults)
