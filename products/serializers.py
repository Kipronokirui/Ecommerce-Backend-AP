from rest_framework import routers, serializers, viewsets
from .models import Category,SubCategory, ManufacturingCompany, Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields = ['id', 'image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image']
    
class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'slug', 'image', 'category']

class ManufacturingCompanySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = ManufacturingCompany
        fields = ['id', 'title', 'slug', 'image', 'sub_category']

class ProductSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturingCompanySerializer()
    category = CategorySerializer(many=True, read_only=True)
    sub_category = SubCategorySerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    # cover_image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'is_discounted', 'discounted_price', 
                  'discount_end_date', 'is_flash_sale', 'flash_sale_price', 'flash_sale_end_date',
                  'slug', 'description', 'cover_image','manufacturer', 'category', 'sub_category', 'images']
        
    def get_images(self, obj):
        request = self.context.get('request')
        product_images = obj.product_images.all()
        serializer = ProductImageSerializer(product_images, many=True, context={'request': request})
        return serializer.data