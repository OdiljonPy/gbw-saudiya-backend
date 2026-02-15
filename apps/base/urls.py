from django.urls import path
from .views import (
    BannerViewSet,
    SponsorshipViewSet,
    MessageViewSet,
    ProductViewSet,
    CategoryViewSet
)

urlpatterns = [
    path('base/banner/',
         BannerViewSet.as_view({'get':'get_banner'}),
         name='get-banner'),
    path('base/sponsorship/',
         SponsorshipViewSet.as_view({'get':'get_sponsorship'}),
         name='get-sponsorship'),
    path('base/message/',
         MessageViewSet.as_view({'post': 'create_message'}),
         name='create-message'),
    path('base/products/category/',
         ProductViewSet.as_view({'get': 'get_products_by_category'}),
         name='get-products-by-category'),
    path('base/products/<int:pk>/',
         ProductViewSet.as_view({'get': 'get_product_detail'}),
         name='get-product-detail'),
    path('base/products/<int:pk>/recommendation/',
         ProductViewSet.as_view({'get': 'get_product_recommendation'}),
         name='get-product-recommendation'
         ),
    path('base/category/',
         CategoryViewSet.as_view({'get': 'get_category_list'}),
         name='get-category-list'
         )

]