from django.shortcuts import render
from rest_framework import routers, serializers, viewsets, status
from .serializers import (Category, CategorySerializer, 
                          SubCategory, SubCategorySerializer,
                          ManufacturingCompany, ManufacturingCompanySerializer,
                          Product, ProductSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.
class CategoryList(APIView):
    def get(self, request, format=None):
        categorys = Category.objects.all()
        category_serializer = CategorySerializer(categorys, many=True, context = {'request':request})
        sub_categorys = SubCategory.objects.all()
        sub_categorys_serializer = SubCategorySerializer(sub_categorys, many=True, context = {'request':request})
        manufacturing_companies = ManufacturingCompany.objects.all()
        manufacturing_companies_serializer = ManufacturingCompanySerializer(manufacturing_companies, many=True, context = {'request':request})
        products = Product.objects.all()
        products_serializer = ProductSerializer(products, many=True, context = {'request':request})

        # Combine the two contexts
        response_data = {
            'categories': category_serializer.data,
            'subcategories': sub_categorys_serializer.data,
            'manufacturing_companies': manufacturing_companies_serializer.data,
            'products': products_serializer.data
        }
        return Response(response_data)
        # return Response(category_serializer.data)

class CategoryDetail(APIView):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        category_serializer = CategorySerializer(category, many=False, context = {'request':request})
        category_products = Product.objects.filter(category=category)
        category_products_serializer = ProductSerializer(category_products, many=True, context = {'request':request})

        response_data = {
            'category': category_serializer.data,
            'category_products': category_products_serializer.data
        }

        return Response(response_data)
    
class ManufacturingCompanyDetail(APIView):
    def get(self, request, slug):
        manufacturer = ManufacturingCompany.objects.get(slug=slug)
        manufacturer_serializer = ManufacturingCompanySerializer(manufacturer, many=False, context = {'request':request})
        manufacturer_products = Product.objects.filter(manufacturer=manufacturer)
        manufacturer_products_serializer = ProductSerializer(manufacturer_products, many=True, context = {'request':request})

        response_data = {
            'manufacturer': manufacturer_serializer.data,
            'manufacturer_products': manufacturer_products_serializer.data
        }

        return Response(response_data)

class ProductDetail(APIView):
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
            product_serializer = ProductSerializer(product, many=False, context = {'request':request})
            related_products = Product.objects.exclude(slug=slug).filter(category__in=product.category.all())
            related_products_serializer = ProductSerializer(related_products, many=True, context = {'request':request})

            response_data = {
                'product': product_serializer.data,
                'related_products': related_products_serializer.data,
            }

            return Response(response_data)
        
        except ValueError:
            return Response({"error": "Invalid slug format"}, status=status.HTTP_400_BAD_REQUEST)