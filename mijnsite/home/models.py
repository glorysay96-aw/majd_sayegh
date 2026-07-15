from django.db import models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from modelcluster.fields import ParentalManyToManyField
from django.db import models
from .blocks import QuizQuestionBlock



class HomePage(Page):
    intro = RichTextField(blank=True)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    about_text = RichTextField(blank=True) 
    contact_info = models.ForeignKey(
        "home.ContactInfo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    reviews = models.ManyToManyField("home.Review", blank=True)
    fb = models.URLField(blank=True, help_text="Plak hier de Facebook link")
    wa = models.URLField(
    blank=True,
    help_text="WhatsApp link"
)
    products = models.ManyToManyField(
    "home.Product",
    blank=True
)    

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("hero_image"),
        FieldPanel("contact_info"),
        FieldPanel("reviews"),
        FieldPanel("about_text"),
        FieldPanel("fb"),
        FieldPanel("wa"),
        FieldPanel("products"),
    ]

class ErvaringenPage(Page):
    tekst = RichTextField(blank=True)

    video = models.URLField(
        blank=True,
        help_text="Plak hier een YouTube link"
    )

    content_panels = Page.content_panels + [
        FieldPanel("tekst"),
        FieldPanel("video"),
    ]
@register_snippet
class ContactInfo(models.Model):
    email = models.EmailField()

    phone_number = models.CharField(max_length=20)

    address = models.CharField(
        max_length=255,
        blank=True
    )

    google_maps_url = models.URLField(
        blank=True,
        help_text="Plak hier Google Maps embed link"
    )

    panels = [
        FieldPanel("email"),
        FieldPanel("phone_number"),
        FieldPanel("address"),
        FieldPanel("google_maps_url"),
    ]

    def __str__(self):
        return "Contact informatie"

class Review(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()

    panels = [
        FieldPanel("name"),
        FieldPanel("text"),
    ]

    def __str__(self):
        return self.name    
    

class ReviewPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]    
@register_snippet
class Product(models.Model):
    naam = models.CharField(max_length=100)
    prijs = models.DecimalField(max_digits=8, decimal_places=2)
    beschrijving = models.TextField(blank=True)

    afbeelding = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel("naam"),
        FieldPanel("prijs"),
        FieldPanel("beschrijving"),
        FieldPanel("afbeelding"),
    ]

    def __str__(self):
        return self.naam

class WebshopPage(Page):
    intro = models.TextField(blank=True)

    products = ParentalManyToManyField(
        "home.Product",
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("products"),
    ]
class Cart(models.Model):
    session_key = models.CharField(max_length=100)

    def totaal(self):
        return sum(item.totaal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    aantal = models.PositiveIntegerField(default=1)

    def totaal(self):
        return self.product.prijs * self.aantal



class QuizPage(Page):

    questions = StreamField(
        [
            ("question", QuizQuestionBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("questions"),
    ]