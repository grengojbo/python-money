from unittest import TestCase
from django_test.models import Entity, Entity_0_USD, Entity_USD
from money.contrib.django.models.fields import NotSupportedLookup
from money import Money, CURRENCY

def pause(): raw_input("Press enter to continue")

class MoneyFieldTestCase(TestCase):
    
    def setUp(self):
        #cleanup all entities
        Entity.objects.all().delete()
        Entity_0_USD.objects.all().delete()
        Entity_USD.objects.all().delete()
        
    
    def assertSameCurrency(self, moneys, currency=None):
        currencies = set([m.currency for m in moneys])
        self.assertTrue(len(currencies) == 1)
        if currency:
            self.assertEqual(currencies.pop().code, currency)
    
    def testCreating(self):
        ind = 0
        for code, currency in CURRENCY.items():
            ind = ind + 1
            price = Money(ind*1000.0, code)
            Entity.objects.create(name=currency.name, price=price)
        count = Entity.objects.all().count()
        self.assertEqual(len(CURRENCY), count)

        for code in CURRENCY:
            count = Entity.objects.filter(price_currency=code).count()
            self.assertTrue(count == 1)
    
    def testRetrive(self):
        price = Money(100, "USD")
        Entity.objects.create(name="one hundred dollars", price=price)
        
        
        #Filter
        qset = Entity.objects.filter(price=price)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, price)
        
        #Get
        entry = Entity.objects.get(price=price)
        self.assertEqual(entry.price, price)
        
        #test retriving without currency
        entry = Entity.objects.get(price=100)
        self.assertEqual(entry.price, price)
    
    def testAssign(self):
        ent = Entity(name='test', price=Money(100, "USD"))
        ent.save()
        self.assertEquals(ent.price, Money(100, "USD"))
        
        ent.price = Money(10, "USD")
        ent.save()
        self.assertEquals(ent.price, Money(10, "USD"))
        
        ent_same = Entity.objects.get(pk=ent.id)
        self.assertEquals(ent_same.price, Money(10, "USD"))
        
    def testDefaults(self):
        ent = Entity_0_USD.objects.create(name='0 USD')
        ent = Entity_0_USD.objects.get(pk=ent.id)
        self.assertEquals(ent.price, Money(0, 'USD'))
        
        ent = Entity_USD.objects.create(name='100 USD', price=100)
        ent = Entity_USD.objects.get(pk=ent.id)
        self.assertEquals(ent.price, Money(100, 'USD'))
        
    def testLookup(self):
        USD100 = Money(100, "USD")
        EUR100 = Money(100, "EUR")
        UAH100 = Money(100, "UAH")
        
        Entity.objects.create(name="one hundred dollars", price=USD100)
        Entity.objects.create(name="one hundred and one dollars", price=USD100+1)
        Entity.objects.create(name="ninety nine dollars", price=USD100-1)
        
        Entity.objects.create(name="one hundred euros", price=EUR100)
        Entity.objects.create(name="one hundred and one euros", price=EUR100+1)
        Entity.objects.create(name="ninety nine euros", price=EUR100-1)
        
        Entity.objects.create(name="one hundred hrivnyas", price=UAH100)
        Entity.objects.create(name="one hundred and one hrivnyas", price=UAH100+1)
        Entity.objects.create(name="ninety nine hrivnyas", price=UAH100-1)
        
        
        #Exact:
        
        qset = Entity.objects.filter(price__exact=USD100)
        self.assertEqual(qset.count(), 1)
        qset = Entity.objects.filter(price__exact=EUR100)
        self.assertEqual(qset.count(), 1)
        qset = Entity.objects.filter(price__exact=UAH100)
        self.assertEqual(qset.count(), 1)
        
        #Less then:
        
        qset = Entity.objects.filter(price__lt=USD100)        
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, USD100-1)
        
        qset = Entity.objects.filter(price__lt=EUR100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, EUR100-1)
        
        qset = Entity.objects.filter(price__lt=UAH100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, UAH100-1)
        
        #Greater then:
        
        qset = Entity.objects.filter(price__gt=USD100)        
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, USD100+1)
        
        qset = Entity.objects.filter(price__gt=EUR100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, EUR100+1)
        
        qset = Entity.objects.filter(price__gt=UAH100)
        self.assertEqual(qset.count(), 1)
        self.assertEqual(qset[0].price, UAH100+1)
        
        #Less then or equal:
        
        qset = Entity.objects.filter(price__lte=USD100)        
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "USD")
        for ent in qset: self.assertTrue(ent.price.amount <= 100)
        
        qset = Entity.objects.filter(price__lte=EUR100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "EUR")
        for ent in qset: self.assertTrue(ent.price.amount <= 100)
        
        qset = Entity.objects.filter(price__lte=UAH100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "UAH")
        for ent in qset: self.assertTrue(ent.price.amount <= 100)
        
        
        #Greater then or equal:
        
        qset = Entity.objects.filter(price__gte=USD100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "USD")
        
        qset = Entity.objects.filter(price__gte=EUR100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "EUR")
        
        qset = Entity.objects.filter(price__gte=UAH100)
        self.assertEqual(qset.count(), 2)
        self.assertSameCurrency([ent.price for ent in qset], "UAH")
        
    def testProxy(self):
        e = Entity()
        e.price = Money(0, "BGN")
        e.price.amount = 3
        self.assertEqual(e.price, Money(3, "BGN"))
        e.price.from_string("BGN 5.0")
        self.assertEqual(e.price, Money(5, "BGN"))
