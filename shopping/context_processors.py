from .models import CartItem, Category, SubCategory

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    return {"cart_count": count}


def categories(request):
    categories = Category.objects.all()
    return {"categories":categories }


def subcategories(request):
    subcategories = SubCategory.objects.all()
    return {"subcategories":subcategories }
