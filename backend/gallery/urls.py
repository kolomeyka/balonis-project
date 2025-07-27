from django.urls import path
from . import views

urlpatterns = [
    # Категории галереи
    path('categories/', views.GalleryCategoryListView.as_view(), name='gallery-categories'),
    
    # Изображения
    path('', views.GalleryImageListView.as_view(), name='gallery-list'),
    path('featured/', views.FeaturedGalleryView.as_view(), name='featured-gallery'),
    path('category/<slug:category_slug>/', views.GalleryByCategoryView.as_view(), name='gallery-by-category'),
    path('<int:pk>/', views.GalleryImageDetailView.as_view(), name='gallery-detail'),
    
    # Отзывы
    path('reviews/', views.ClientReviewListView.as_view(), name='client-reviews'),
    path('reviews/featured/', views.FeaturedReviewsView.as_view(), name='featured-reviews'),
    path('reviews/create/', views.ClientReviewCreateView.as_view(), name='create-review'),
]

