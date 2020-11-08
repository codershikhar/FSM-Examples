from django.test import TestCase, Client
from django.urls import reverse
from fsm_order.models import Order


class TestHomeViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.order_home_url = reverse('order_home')

    def test_order_home_view_GET(self):
        response = self.client.get(self.order_home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_home.html')


class TestCreateOrderViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.create_order_url = reverse('create_order')

    def test_create_order_view_POST(self):
        response = self.client.post(self.create_order_url, {
            'amount': 1001,
            'product': 'Test 1'
        })

        order = Order.objects.get(id=1)

        self.assertEquals(response.status_code, 201)
        self.assertTemplateUsed(response, 'order_status.html')
        self.assertEquals(order.amount, 1001)
        self.assertEquals(order.product, 'Test 1')
        self.assertEquals(order.status, 0)

    def test_create_order_view_no_amount_POST(self):
        response = self.client.post(self.create_order_url, {
            'product': 'Test'
        })

        self.assertEquals(response.status_code, 500)
        self.assertTemplateUsed(response, 'order_home.html')

    def test_create_order_view_no_product_POST(self):
        response = self.client.post(self.create_order_url, {
            'amount': 1000
        })

        self.assertEquals(response.status_code, 500)
        self.assertTemplateUsed(response, 'order_home.html')

    def test_create_order_view_no_body_POST(self):
        response = self.client.post(self.create_order_url, {})

        self.assertEquals(response.status_code, 500)
        self.assertTemplateUsed(response, 'order_home.html')


class TestPayOrderViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.pay_order_url = reverse('pay_order')

    def test_pay_order_view_with_created_status_POST(self):
        order_created = Order.objects.create(
            amount=1000,
            product='Test',
            status=0
        )

        response = self.client.post(self.pay_order_url, {
            'order_id': order_created.id
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_pay_order_view_with_paid_status_POST(self):
        order_paid = Order.objects.create(
            amount=1000,
            product='Test',
            status=1
        )

        response = self.client.post(self.pay_order_url, {
            'order_id': order_paid.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_pay_order_view_with_fulfilled_status_POST(self):
        order_fulfilled = Order.objects.create(
            amount=1000,
            product='Test',
            status=2
        )

        response = self.client.post(self.pay_order_url, {
            'order_id': order_fulfilled.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_pay_order_view_with_cancelled_status_POST(self):
        order_cancelled = Order.objects.create(
            amount=1000,
            product='Test',
            status=3
        )

        response = self.client.post(self.pay_order_url, {
            'order_id': order_cancelled.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_pay_order_view_with_returned_status_POST(self):
        order_returned = Order.objects.create(
            amount=1000,
            product='Test',
            status=4
        )

        response = self.client.post(self.pay_order_url, {
            'order_id': order_returned.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_pay_order_view_with_no_body_POST(self):
        response = self.client.post(self.pay_order_url, {})

        self.assertEquals(response.status_code, 500)
        self.assertTemplateUsed(response, 'order_status.html')


class TestFulfillOrderViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.fulfill_order_url = reverse('fulfill_order')

    def test_fulfill_order_view_with_created_status_POST(self):
        order_created = Order.objects.create(
            amount=1000,
            product='Test',
            status=0
        )

        response = self.client.post(self.fulfill_order_url, {
            'order_id': order_created.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_fulfill_order_view_with_paid_status_POST(self):
        order_paid = Order.objects.create(
            amount=1000,
            product='Test',
            status=1
        )

        response = self.client.post(self.fulfill_order_url, {
            'order_id': order_paid.id
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_fulfill_order_view_with_fulfilled_status_POST(self):
        order_fulfilled = Order.objects.create(
            amount=1000,
            product='Test',
            status=2
        )

        response = self.client.post(self.fulfill_order_url, {
            'order_id': order_fulfilled.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_fulfill_order_view_with_cancelled_status_POST(self):
        order_cancelled = Order.objects.create(
            amount=1000,
            product='Test',
            status=3
        )

        response = self.client.post(self.fulfill_order_url, {
            'order_id': order_cancelled.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_fulfill_order_view_with_returned_status_POST(self):
        order_returned = Order.objects.create(
            amount=1000,
            product='Test',
            status=4
        )

        response = self.client.post(self.fulfill_order_url, {
            'order_id': order_returned.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_fulfill_order_view_with_no_body_POST(self):
        response = self.client.post(self.fulfill_order_url, {})

        self.assertEquals(response.status_code, 500)
        self.assertTemplateUsed(response, 'order_status.html')


class TestCancelOrderViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.cancel_order_url = reverse('cancel_order')

    def test_cancel_order_view_with_created_status_POST(self):
        order_created = Order.objects.create(
            amount=1000,
            product='Test',
            status=0
        )

        response = self.client.post(self.cancel_order_url, {
            'order_id': order_created.id
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_cancel_order_view_with_paid_status_POST(self):
        order_paid = Order.objects.create(
            amount=1000,
            product='Test',
            status=1
        )

        response = self.client.post(self.cancel_order_url, {
            'order_id': order_paid.id
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_cancel_order_view_with_fulfilled_status_POST(self):
        order_fulfilled = Order.objects.create(
            amount=1000,
            product='Test',
            status=2
        )

        response = self.client.post(self.cancel_order_url, {
            'order_id': order_fulfilled.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_cancel_order_view_with_cancelled_status_POST(self):
        order_cancelled = Order.objects.create(
            amount=1000,
            product='Test',
            status=3
        )

        response = self.client.post(self.cancel_order_url, {
            'order_id': order_cancelled.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_cancel_order_view_with_returned_status_POST(self):
        order_returned = Order.objects.create(
            amount=1000,
            product='Test',
            status=4
        )

        response = self.client.post(self.cancel_order_url, {
            'order_id': order_returned.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_cancel_order_view_with_no_body_POST(self):
        response = self.client.post(self.cancel_order_url, {})

        self.assertEquals(response.status_code, 500)
        self.assertTemplateUsed(response, 'order_status.html')


class TestReturnOrderViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.return_order_url = reverse('return_order')

    def test_return_order_view_with_created_status_POST(self):
        order_created = Order.objects.create(
            amount=1000,
            product='Test',
            status=0
        )

        response = self.client.post(self.return_order_url, {
            'order_id': order_created.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_return_order_view_with_paid_status_POST(self):
        order_paid = Order.objects.create(
            amount=1000,
            product='Test',
            status=1
        )

        response = self.client.post(self.return_order_url, {
            'order_id': order_paid.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_return_order_view_with_fulfilled_status_POST(self):
        order_fulfilled = Order.objects.create(
            amount=1000,
            product='Test',
            status=2
        )

        response = self.client.post(self.return_order_url, {
            'order_id': order_fulfilled.id
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_return_order_view_with_cancelled_status_POST(self):
        order_cancelled = Order.objects.create(
            amount=1000,
            product='Test',
            status=3
        )

        response = self.client.post(self.return_order_url, {
            'order_id': order_cancelled.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_return_order_view_with_returned_status_POST(self):
        order_returned = Order.objects.create(
            amount=1000,
            product='Test',
            status=4
        )

        response = self.client.post(self.return_order_url, {
            'order_id': order_returned.id
        })

        self.assertEquals(response.status_code, 400)
        self.assertTemplateUsed(response, 'order_status.html')

    def test_return_order_view_with_no_body_POST(self):
        response = self.client.post(self.return_order_url, {})

        self.assertEquals(response.status_code, 500)
        self.assertTemplateUsed(response, 'order_status.html')
