from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product
from .forms import ProductForm

def admin_only(user):
    return user.is_authenticated and getattr(user, "role", "user") == "admin"

@login_required
def product_list(request):
    q = request.GET.get("q", "").strip()
    qs = Product.objects.all().order_by("-created_at")
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(category__icontains=q))
    return render(request, "products/list.html", {"rows": qs, "q": q})

@login_required
def product_create(request):
    if not admin_only(request.user):
        messages.error(request, "Admin only.")
        return redirect("product_list")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added.")
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "products/form.html", {"form": form, "mode": "create"})

@login_required
def product_edit(request, pk):
    if not admin_only(request.user):
        messages.error(request, "Admin only.")
        return redirect("product_list")

    obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated.")
            return redirect("product_list")
    else:
        form = ProductForm(instance=obj)
    return render(request, "products/form.html", {"form": form, "mode": "edit"})

@login_required
def product_delete(request, pk):
    if not admin_only(request.user):
        messages.error(request, "Admin only.")
        return redirect("product_list")

    obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.info(request, "Product deleted.")
    return redirect("product_list")

@login_required
def cart_add(request, pk):
    cart = request.session.get("cart", {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session["cart"] = cart
    messages.success(request, "Added to cart.")
    return redirect("product_list")