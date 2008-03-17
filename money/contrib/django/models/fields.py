from django.db import models
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
            #setattr(obj, self.currency_field_name, value.currency)
        else:
            obj.__dict__[self.field.name] = self.field.to_python(value) 


class MoneyField(models.DecimalField):
    
    #TODO: is tehre any options for __init__ ? (f.e. indexing, defaults, etc.)
    
    def get_internal_type(self): 
         return "DecimalField"
     
    def contribute_to_class(self, cls, name):
        c_field_name = currency_field_name(name)
        c_field = models.CharField(max_length=3)
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
