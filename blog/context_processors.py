from .models import Category

def category_model(request):
    return {'categories': Category.objects.all()}