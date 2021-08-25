from django.contrib import admin
from .models import Coin


# Register your models here.

class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'symbol', 'url', 'status')


admin.site.register(Coin, CoinAdmin)
