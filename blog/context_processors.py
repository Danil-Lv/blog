from .models import Category

def category_model(request):
    """Вывод категорий в шапке"""
    return {'categories': Category.objects.all()}