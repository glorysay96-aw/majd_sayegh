from django.db import models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


class HomePage(Page):
    intro = RichTextField(blank=True)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
     
    contact_info = models.ForeignKey(
        "home.ContactInfo",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    reviews = models.ManyToManyField("home.Review", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("hero_image"),
        FieldPanel("contact_info"),
        FieldPanel("reviews"),
    ]

class ErvaringenPage(Page):
    tekst = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("tekst"),
    ]

@register_snippet
class ContactInfo(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    panels = [
        FieldPanel("email"),
        FieldPanel("phone_number"),
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