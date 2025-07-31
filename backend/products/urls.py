from django.urls import path
from . import views

urlpatterns = [
    # Категории, цвета, источники
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('colors/', views.ColorListView.as_view(), name='color-list'),
    path('sources/', views.SourceListView.as_view(), name='source-list'),
    
    # Товары
    path('', views.ProductListView.as_view(), name='product-list'),
    path('featured/', views.FeaturedProductsView.as_view(), name='featured-products'),
    path('popular/', views.PopularProductsView.as_view(), name='popular-products'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Отзывы
    # path('<int:product_id>/reviews/', views.ReviewListCreateView.as_view(), name='product-reviews'),
    
    # Утилиты
    path('filters/', views.product_filters, name='product-filters'),
    path('search/', views.search_products, name='product-search'),
]

