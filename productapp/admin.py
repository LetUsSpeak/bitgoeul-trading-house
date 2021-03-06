from django.contrib import admin

# Register your models here.
from productapp.models import Product, Category

admin.site.register(Product)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)