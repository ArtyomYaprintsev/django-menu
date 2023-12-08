from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Menu(models.Model):
    """Menu is represented by this model."""

    slug = models.SlugField(_("slug"), max_length=25, unique=True)

    class Meta:
        verbose_name = _("menu")
        verbose_name_plural = _("menus")

    def __str__(self) -> str:
        return self.slug


class Item(models.Model):
    """Menu item is represented by this model.

    Can be related with another menu item as child item.
    """

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        verbose_name=_("menu"),
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name=_("parent item"),
        null=True,
        blank=True,
        default=None,
        help_text=_(
            "The missing parent item means that this item is the root item "
            "in the related menu.",
        ),
    )

    title = models.CharField(_("title"), max_length=25)

    class Meta:
        verbose_name = _("item")
        verbose_name_plural = _("items")

    def __str__(self) -> str:
        return f"#{self.pk} [{self.title}]"

    def clean(self) -> None:
        # Check on save that item and parent menus are equal 
        if self.parent and self.menu != self.parent.menu:
            raise ValidationError(
                _(
                    "Item and parent menus must be equal. Parent menu is "
                    "\"%(menu)s\".",
                ),
                params={
                    "menu": str(self.parent.menu),
                },
            )

        return super().clean()
