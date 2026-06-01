from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review
from home.models import Product

def review_page(request):
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.path)

    reviews = Review.objects.all()

    return render(request, "home/reviews_page.html", {
        "form": form,
        "reviews": reviews
    })


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER", "/"))
   


def cart_view(request):
    cart = request.session.get("cart", {})

    products = []
    totaal = 0

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        product.qty = qty
        product.subtotal = product.prijs * qty

        totaal += product.subtotal
        products.append(product)

    return render(request, "home/cart.html", {
        "products": products,
        "totaal": totaal
    })
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")