from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.index,name="index" ),
    
    
    path('cartdetails/',views.view_cart, name="cartdetails"),
    path(" productdetail/<int:id>/",views.product_detail, name="product_detail"),
    path("search/", views.search, name="search"),
    path('subcategory_products/<int:id>/',views.subcategory_products,name="subcategory_products"),
    path('contact/', views.contact_view,name="contact"),
    
    path('login/',views.login_view,name="login"),
    path('register/',views.register_view,name="register"),
    path('logout/',views.logout_view,name="logout"),
    
    
    
    #  For Cart urls
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cartdetails/',views.view_cart, name="cartdetails"),
    path('increase_quantity/<int:item_id>/',views.increase_quantity,name="increase_quantity"),
    path('decrease_quantity/<int:item_id>/',views.decrease_quantity,name = "decrease_quantity"),
    path('remove_from_cart/<int:item_id>/',views.remove_from_cart,name = "remove_from_cart"),
   
   

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)