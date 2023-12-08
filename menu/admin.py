from django.contrib import admin

from menu.models import Menu, Item


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
