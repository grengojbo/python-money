from django import newforms as forms
from money import Money, CURRENCY
from decimal import Decimal

__all__ = ('InputMoneyWidget', 'CurrencySelect',)

CURRENCY_CHOICES = ((c.code, c.name) for i, c in CURRENCY.items() if c.code != 'XXX')

class CurrencySelect(forms.Select):
    def __init__(self, attrs=None, choices=CURRENCY_CHOICES):
        super(CurrencySelect, self).__init__(attrs, choices)
    
class InputMoneyWidget(forms.TextInput):
    
    def __init__(self, attrs=None, currency_widget=None):
        self.currency_widget = currency_widget
        if not self.currency_widget:
            self.currency_widget = CurrencySelect()
        super(InputMoneyWidget, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        amount = ''
        currency = ''
        if isinstance(value, Money):
            amount = value.amount
            currency = value.currency.code
        if isinstance(value, tuple):
            amount = value[0]
            currency = value[1]
        if isinstance(value, int) or isinstance(value, Decimal):
            amount = value
        result = super(InputMoneyWidget, self).render(name, amount)
        result += self.currency_widget.render(name+'_currency', currency)
        return result
    
    def value_from_datadict(self, data, files, name):
        return (data.get(name, None), data.get(name+'_currency', None))
