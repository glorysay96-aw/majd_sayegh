from django.db import models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class HomePage(Page):
    intro = RichTextField(blank=True)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("hero_image"),
    ]

class ErvaringenPage(Page):
    tekst = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("tekst"),
    ]