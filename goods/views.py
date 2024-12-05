from django.views.generic import DetailView, ListView
from goods.models import Category, Product


class CategoryView(ListView):
    model = Category
    template_name = 'goods/categories.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**self.kwargs)
        context['title'] = 'PC-Shop - Catalog'
        return context



class ProductView(DetailView):
    ...

class CatalogView(DetailView):
    ...
