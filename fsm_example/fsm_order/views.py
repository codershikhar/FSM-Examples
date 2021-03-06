from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order
import traceback
from django_fsm import TransitionNotAllowed


def order_home(request):
    try:
        orders = Order.objects.all()
        print('orders', orders)
        return render(request, 'order_home.html', {'orders': orders}, status=200)
    except Exception:
        traceback.print_exc()
        return render(request, 'order_home.html', {'error': 'Something went wrong!'}, status=500)


def create_order(request):
    try:
        order = Order(amount=request.POST['amount'], product=request.POST['product'])
        order.save()
        return render(request, 'order_status.html', {'message': 'Order Created', 'order': order}, status=201)
    except Exception:
        traceback.print_exc()
        return render(request, 'order_home.html', {'error': 'Order Creation Failed!'}, status=500)


def pay_order(request):
    try:
        order_id = request.POST['order_id']
        order = Order.objects.get(pk=order_id)

        # transition
        order.pay()
        order.save()

        return render(request, 'order_status.html', {'message': 'Order Payed', 'order': order}, status=200)
    except TransitionNotAllowed:
        traceback.print_exc()
        print('order', order)
        data = {'error': f'Transition from {order.get_status_display()} to Pay not allowed!', 'order': order}
        return render(request, 'order_status.html', data, status=400)
    except Exception:
        traceback.print_exc()
        return render(request, 'order_status.html', {'error': 'Something went wrong while paying for Order!'},
                      status=500)


def fulfill_order(request):
    try:
        order_id = request.POST['order_id']
        order = Order.objects.get(pk=order_id)

        # transition
        order.fulfill()
        order.save()

        return render(request, 'order_status.html', {'message': 'Order Fulfilled', 'order': order}, status=200)
    except TransitionNotAllowed:
        traceback.print_exc()
        data = {'error': f'Transition from {order.get_status_display()} to Fulfill not allowed!', 'order': order}
        return render(request, 'order_status.html', data, status=400)
    except Exception:
        traceback.print_exc()
        return render(request, 'order_status.html', {'error': 'Something went wrong while fulfilling the Order!'},
                      status=500)


def cancel_order(request):
    try:
        order_id = request.POST['order_id']
        order = Order.objects.get(pk=order_id)

        # transition
        order.cancel()
        order.save()

        return render(request, 'order_status.html', {'message': 'Order Canceled', 'order': order}, status=200)
    except TransitionNotAllowed:
        traceback.print_exc()
        data = {'error': f'Transition from {order.get_status_display()} to Cancel not allowed!', 'order': order}
        return render(request, 'order_status.html', data, status=400)
    except Exception:
        traceback.print_exc()
        return render(request, 'order_status.html', {'error': 'Something went wrong while canceling Order!'},
                      status=500)


def return_order(request):
    try:
        order_id = request.POST['order_id']
        order = Order.objects.get(pk=order_id)

        # transition
        order.return_order()
        order.save()

        return render(request, 'order_status.html', {'message': 'Order Returned', 'order': order}, status=200)
    except TransitionNotAllowed:
        traceback.print_exc()
        data = {'error': f'Transition from {order.get_status_display()} to Return not allowed!', 'order': order}
        return render(request, 'order_status.html', data, status=400)
    except Exception:
        traceback.print_exc()
        return render(request, 'order_status.html', {'error': 'Something went wrong while returning Order!'},
                      status=500)
