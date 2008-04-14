from django.utils.translation import ugettext_lazy as _
from django import newforms as forms
from widgets import InputMoneyWidget
from money import Money, CURRENCY

__all__ = ('MoneyField',)

class MoneyField(forms.DecimalField):
    
    def __init__(self, currency_widget=None, *args, **kwargs):
        self.widget = InputMoneyWidget(currency_widget=currency_widget)
        super(MoneyField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        if not isinstance(value, tuple):
            raise Exception("Invalid value provided for MoneyField.clean (expected tupple)")
        amount = super(MoneyField, self).clean(value[0])
        currency = value[1]
        if not currency:
            raise forms.ValidationError(_(u'Input currency'))
        currency = currency.upper()
        if not CURRENCY.get(currency, False) or currency == u'XXX':
            raise forms.ValidationError(_(u'This currency not exist'))
        return Money(amount=amount, currency=currency)