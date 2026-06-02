from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review
from home.models import Product
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse



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

def checkout(request):
    cart = request.session.get("cart", {})

    producten = []
    totaal = 0

    for product_id, aantal in cart.items():
        product = Product.objects.get(id=product_id)

        subtotaal = product.prijs * aantal
        totaal += subtotaal

        producten.append({
            "product": product,
            "aantal": aantal,
            "subtotaal": subtotaal,
        })

    return render(
        request,
        "home/checkout.html",
        {
            "producten": producten,
            "totaal": totaal,
        },
    )   

def start_mollie_payment(request):
    try:
        from mollie.api.client import Client 
        client = Client()
        client.set_api_key(settings.MOLLIE_API_KEY)

        payment = client.payments.create({
            "amount": {
                "currency": "EUR",
                "value": "1.00"
            },
            "description": "Webshop bestelling",
            "redirectUrl": "https://majdsayegh.nl/payment/success/",
        })

        if not payment or not hasattr(payment, "checkout_url"):
            return HttpResponse("www.mollie.com/checkout")

        return redirect(payment.checkout_url)

    except Exception as e:
        return HttpResponse(f"Mollie error: {str(e)}")


def payment_success(request):
    return HttpResponse("🎉 Betaling geslaagd!")