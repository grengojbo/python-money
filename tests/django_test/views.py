from django import newforms as forms
from django.shortcuts import render_to_response
from money.contrib.django.forms.fields import MoneyField
from money import Money

class TestForm(forms.Form):
    price = MoneyField()



def form1(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            price = form.cleaned_data['price']
            print price
            return render_to_response('form1.html', {'price':price} )
    else:
        form = TestForm()
    return  render_to_response('form1.html', {'form':form} )