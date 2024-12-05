from django.urls import path
from goods.views import CategoryView, CatalogView, ProductView

app_name = 'goods'

urlpatterns = [
    path('search/', CatalogView.as_view(), name='search'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('catalog/<slug:catalog_slug>', CatalogView.as_view(), name='catalog'),
    path('product/<slug:product_slug>', ProductView.as_view(), name='product'),
]
