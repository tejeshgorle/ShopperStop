from django.contrib import admin
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group 

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'category', 'product_image']
    search_fields = ['title', 'category']
    list_filter = ['category']
    readonly_fields = ['id']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_link', 'quantity']  # Use product_link

    def product_link(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

    product_link.short_description = "Product"  # This sets the column header in the admin panel


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']    


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer_link', 'product_link', 'quantity', 'ordered_date', 'status', 'payment_link', 'total_cost']  
    search_fields = ['user__username', 'customer__name', 'product__title']  # Ensure correct field names
    list_filter = ['status', 'ordered_date'] 

    def total_cost(self, obj):
        return obj.total_cost  # Ensure this is correctly defined in your model

    total_cost.admin_order_field = 'quantity'  
    total_cost.short_description = 'Total Cost'

    def customer_link(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)  # Use correct field
    customer_link.short_description = "Customer"

    def product_link(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)  # Ensure correct field
    product_link.short_description = "Product"

    def payment_link(self, obj):
        link = reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>', link, str(obj.payment))  # Ensure correct field
    payment_link.short_description = "Payment"



@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']
    def product_link(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

    product_link.short_description = "Product"

admin.site.unregister(Group)