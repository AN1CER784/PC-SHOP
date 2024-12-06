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
    model = Product
    template_name = 'goods/product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'

    def get_object(self, queryset=None):
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'PC-Shop - {self.object.name}'
        return context


class CatalogView(ListView):
    model = Product
    template_name = 'goods/catalog.html'
    context_object_name = 'products'
    slug_url_kwarg = 'catalog_slug'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'PC-Shop - Catalog'
        return context

    def get_queryset(self):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug == 'all':
            goods = Product.objects.all()
        else:
            goods = Product.objects.filter(category__slug=slug)
        return goods
