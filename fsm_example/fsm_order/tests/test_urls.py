from django.test import SimpleTestCase
from django.urls import reverse, resolve
from fsm_order.views import order_home, create_order, pay_order, fulfill_order, cancel_order, return_order


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('order_home')
        self.assertEquals(resolve(url).func, order_home)

    def test_create_order_url_resolves(self):
        url = reverse('create_order')
        self.assertEquals(resolve(url).func, create_order)

    def test_pay_order_url_resolves(self):
        url = reverse('pay_order')
        self.assertEquals(resolve(url).func, pay_order)

    def test_fulfill_order_url_resolves(self):
        url = reverse('fulfill_order')
        self.assertEquals(resolve(url).func, fulfill_order)

    def test_cancel_order_url_resolves(self):
        url = reverse('cancel_order')
        self.assertEquals(resolve(url).func, cancel_order)

    def test_return_order_url_resolves(self):
        url = reverse('return_order')
        self.assertEquals(resolve(url).func, return_order)
