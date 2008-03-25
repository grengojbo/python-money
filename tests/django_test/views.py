from django import newforms as forms
from django.shortcuts import render_to_response, get_object_or_404
from money.contrib.django.forms.fields import MoneyField
from money import Money


#regular form

class TestForm(forms.Form):
    price = MoneyField()


#ModelForm
from django_test.models import Entity    
class TestModelForm(forms.ModelForm):
    class Meta:
        model = Entity




def regular_form(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            price = form.cleaned_data['price']
            return render_to_response('form.html', {'price':price} )
    else:
        form = TestForm()
    return  render_to_response('form.html', {'form':form} )

def regular_form_edit(request, id):
    instance = get_object_or_404(Entity, pk=id)
    if request.method == 'POST':
        form = TestForm(request.POST, initial={'price':instance.price})
        print form.is_valid()
        if form.is_valid():
            price = form.cleaned_data['price']
            return render_to_response('form.html', {'price':price} )
    else:
        form = TestForm(initial={'price':instance.price})
    return  render_to_response('form.html', {'form':form} )

def model_form(request):
    if request.method == 'POST':
        form = TestModelForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            price = form.cleaned_data['price']
            form.save()
            return render_to_response('form.html', {'price':price} )
    else:
        form = TestModelForm()
    return  render_to_response('form.html', {'form':form} )

def model_form_edit(request, id):
    instance = get_object_or_404(Entity, pk=id)
    if request.method == 'POST':
        form = TestModelForm(request.POST, instance=instance)
        print form.is_valid()
        if form.is_valid():
            price = form.cleaned_data['price']
            form.save()
            return render_to_response('form.html', {'price':price} )
    else:
        form = TestModelForm(instance=instance)
    return  render_to_response('form.html', {'form':form} )
