from django.shortcuts import render, redirect
from .forms import ReviewForm
from .models import Review

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