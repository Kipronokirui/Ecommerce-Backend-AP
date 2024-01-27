from django.urls import path
# from django.urls import url
from . import views 

urlpatterns = [
    path('', views.CategoryList.as_view(), name='home'),
    path('product/<str:slug>/', views.ProductDetail.as_view(), name='product-detail'),
    path('category/<str:slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('company/<str:slug>/', views.ManufacturingCompanyDetail.as_view(), name='company-detail'),
]