from django.urls import path
from .views import (
    BannerViewSet,
    SponsorshipViewSet,
    MessageViewSet,
    ProductViewSet,
    CategoryViewSet,
    AboutUsViewSet,
    OrderViewSet
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
    path('base/products/<int:pk>/recommendation/',
         ProductViewSet.as_view({'get': 'get_product_recommendation'}),
         name='get-product-recommendation'
         ),
    path('base/category/',
         CategoryViewSet.as_view({'get': 'get_category_list'}),
         name='get-category-list'
         ),
    path('base/category/<int:pk>/',
         CategoryViewSet.as_view({'get': 'get_category_detail'}),
         name='get-category-detail'),

    path('base/about_us/',
         AboutUsViewSet.as_view({'get': 'get_about_us'}),
         name='get-about-us'),
    path('base/order/',
         OrderViewSet.as_view({'post': 'create_order'}),
         name='create-order'),

]