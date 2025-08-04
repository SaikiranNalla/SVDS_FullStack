from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, OrdersForm
from .models import Orders
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'mysite/home.html')

@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    tabs = [
        {
          'key': 'pending',
          'label': 'Pending',
          'orders': Orders.objects.filter(delivery_status='pending').order_by('-date'),
        },
        {
          'key': 'delivered',
          'label': 'Delivered',
          'orders': Orders.objects.filter(delivery_status='completed').order_by('-date'),
        },
        {
          'key': 'unpaid',
          'label': 'Unpaid',
          'orders': Orders.objects.filter(payment_status='pending').order_by('-date'),
        },
        {
          'key': 'paid',
          'label': 'Paid',
          'orders': Orders.objects.filter(payment_status='paid').order_by('-date'),
        },
    ]
    return render(request, 'mysite/dashboard.html', {'tabs': tabs})
# def dashboard(request):
#     """
#     Renders the admin dashboard with four tabs:
#       - pending delivery
#       - delivered
#       - unpaid
#       - paid
#     """
#     # 1) Fetch querysets for each tab
#     pending_delivery = Orders.objects.filter(delivery_status='pending').order_by('-date')
#     delivered       = Orders.objects.filter(delivery_status='completed').order_by('-date')
#     unpaid          = Orders.objects.filter(payment_status='pending').order_by('-date')
#     paid            = Orders.objects.filter(payment_status='paid').order_by('-date')
#
#     # 2) Package them into a dict keyed by the template’s tab IDs
#     orders_by_status = {
#         'pending': pending_delivery,
#         'delivered': delivered,
#         'unpaid': unpaid,
#         'paid': paid,
#     }
#
#     # A list of (key, label) for your nav‑pills
#     status_tabs = [
#         ('pending',   'Pending'),
#         ('delivered', 'Delivered'),
#         ('unpaid',    'Unpaid'),
#         ('paid',      'Paid'),
#     ]
#     return render(request, 'mysite/dashboard.html', {
#         'orders_by_status': orders_by_status,
#         'status_tabs': status_tabs,
#     })

@login_required
@user_passes_test(lambda u: u.is_staff)
def addtransit(request):
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Transit order saved successfully.")
            return redirect('mysite:dashboard')
    else:
        form = OrdersForm()
    return render(request, 'mysite/addtransit.html', {'form': form})


from django.shortcuts import get_object_or_404

@login_required
@user_passes_test(lambda u: u.is_staff)
def edittransit(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)

    if request.method == 'POST':
        form = OrdersForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Transit {order.svds_bill_no} updated.")
            return redirect('mysite:dashboard')
    else:
        form = OrdersForm(instance=order)

    return render(request, 'mysite/edittransit.html', {
        'form': form,
        'order': order,
    })


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('mysite:dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {"form": form})

def careers(request):
    return render(request, 'mysite/careers.html')


# To generate pdf
from django.http import HttpResponse
from .models import Orders
from .bills import create_bill  # If your PDF function is in bills.py
from io import BytesIO

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_bill_pdf(request, order_id):
    # 1. Make sure the order exists
    order = get_object_or_404(Orders, pk=order_id)

    # 2. Create in‑memory buffer
    buffer = BytesIO()

    # 3. Generate the PDF into that buffer
    #    We pass buffer instead of a filename—ReportLab writes into it directly.
    # create_bill_pdf(order_id=order.pk, output_path=buffer)
    create_bill(order_id=order.pk, output_path=buffer)  # ← Correct function

    # 4. Get PDF contents & close buffer
    pdf_bytes = buffer.getvalue()
    buffer.close()

    # 5. Build the HTTP response
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    #   inline = display in browser; attachment = download prompt
    filename = f"SVDS_{order.svds_bill_no}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response



# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from .forms import OrderForm
# from .models import Orders
# PDF generation import placeholder (e.g. WeasyPrint)


# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('orders:dashboard')
#     msg = None
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('orders:dashboard')
#         else:
#             msg = 'Invalid credentials'
#     return render(request, 'mysite/login.html', {'error': msg})
#
#
# def logout_view(request):
#     logout(request)
#     return redirect('orders:login')
#
# @login_required
# def dashboard(request):
#     pending = Order.objects.filter(status='pending')
#     completed = Order.objects.filter(status='completed')
#     return render(request, 'orders/admin_dashboard.html', {
#         'pending': pending, 'completed': completed
#     })
#
# @login_required
# def add_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('orders:dashboard')
#     else:
#         form = OrderForm()
#     return render(request, 'orders/order_form.html', {'form': form})
#
# @login_required
# def complete_order(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     if request.method == 'POST':
#         order.other_charges = int(request.POST.get('other_charges', 0))
#         order.freight_charges = int(request.POST.get('freight_charges', 0))
#         order.total_charge = order.vehicle_charge + order.freight_charges + order.other_charges
#         order.status = 'completed'
#         # generate PDF here and set invoice_number
#         order.invoice_number = f"INV{order.id:05d}"
#         order.save()
#         return redirect('orders:dashboard')
#     return render(request, 'orders/complete_order.html', {'order': order})
#
# @login_required
# def download_invoice(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     # render PDF response
#     # pdf = render_to_pdf('orders/invoice_template.html', {'order': order})
#     # return HttpResponse(pdf, content_type='application/pdf')
#     pass
