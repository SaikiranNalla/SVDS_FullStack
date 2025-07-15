from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'mysite/home.html')


from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    pass


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from .forms import OrderForm
# from .models import Order
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
#     return render(request, 'login.html', {'error': msg})
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
