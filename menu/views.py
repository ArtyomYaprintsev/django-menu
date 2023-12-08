from django.shortcuts import render

from menu.models import Menu


def show_menus(request):
    return render(request, 'menus.html', context={
        "menus": Menu.objects.all(),
    })
