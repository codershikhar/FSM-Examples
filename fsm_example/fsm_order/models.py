from django.db import models
from django_fsm import transition, FSMIntegerField


class Order(models.Model):
    STATUS_CREATED = 0
    STATUS_PAID = 1
    STATUS_FULFILLED = 2
    STATUS_CANCELLED = 3
    STATUS_RETURNED = 4
    STATUS_CHOICES = (
        (STATUS_CREATED, 'created'),
        (STATUS_PAID, 'paid'),
        (STATUS_FULFILLED, 'fulfilled'),
        (STATUS_CANCELLED, 'cancelled'),
        (STATUS_RETURNED, 'returned'),
    )
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    product = models.CharField(max_length=200)
    status = FSMIntegerField(choices=STATUS_CHOICES, default=STATUS_CREATED, protected=True)

    @transition(field=status, source=STATUS_CREATED, target=STATUS_PAID)
    def pay(self):
        print("Pay the order")

    @transition(field=status, source=STATUS_PAID, target=STATUS_FULFILLED)
    def fulfill(self):
        print("Fulfill the order")

    @transition(field=status, source=[STATUS_CREATED, STATUS_PAID], target=STATUS_CANCELLED)
    def cancel(self):
        print("Cancel the order")

    @transition(field=status, source=STATUS_FULFILLED, target=STATUS_RETURNED)
    def _return(self):
        print("Return the order")
