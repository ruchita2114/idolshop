from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Product, Category, Order, OrderItem
from .cart import Cart


def home(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "home.html", {"products": products})


def product_list(request):
    query = request.GET.get("q")
    category = request.GET.get("category")

    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category:
        products = products.filter(category__id=category)

    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories,
        "query": query,
        "selected_category": category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "products/product_detail.html", {
        "product": product
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect("products:cart_detail")


@require_POST
def cart_decrease(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product, quantity=1)
    return redirect("products:cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    while str(product.id) in cart.cart:
        cart.remove(product)

    return redirect("products:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "products/cart_detail.html", {
        "cart": cart
    })


def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("products:cart_detail")

    if request.method == "POST":

        order = Order.objects.create(
            full_name=request.POST["full_name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            address=request.POST["address"],
            city=request.POST["city"],
            pincode=request.POST["pincode"],
            total_price=cart.get_total_price(),
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["price"],
                quantity=item["quantity"],
            )

        cart.clear()

        return render(request, "products/order_success.html", {
            "order": order
        })

    return render(request, "products/checkout.html")