from django.contrib import admin
from .models import Category,SubCategory,Product,CartItem,Contact

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Contact)