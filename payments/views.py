from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters, generics, permissions, status
from django.contrib.auth.models import User
from .serializers import (Order, OrderSerializer, 
                          OrderItem, OrderItemSerializer, 
                          Product, ProductSerializer)
from users.serializers import (User, UserSerializer)
# products=[
#         {
#             'qty':2,
#             "product":{
#                 "id":1,
#                 "title":"Samsung Phone"
#             }
#         },
#         {
#             'qty':4,
#             "product":{
#                 "id":2,
#                 "title":"django rest framework",
#             }
#         },
# ]

# Create your views here.
class OrdersList(APIView):
    def get(self, request, format=None):
        orders=Order.objects.all()
        orders_serializer=OrderSerializer(orders, many=True)
        data={
            "orders":orders_serializer.data,
        }
        return Response(data)

class UserOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        try:
            user_id = request.user.id
            user_usename = 'admin'
            user = User.objects.get(id=user_id)
            orders=Order.objects.filter(user=user)
            orders_serializer=OrderSerializer(orders, many=True)
            data={
                "orders":orders_serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        
class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        try:
            user_id = request.user.id
            user_usename = 'admin'
            user = User.objects.get(id=user_id)
            if request.method == 'POST':
                products = request.data
                if not products:
                    print("Cart cannot be empty")
                    return Response("Empty cart", status=status.HTTP_400_BAD_REQUEST)
                # print(products)
                total_price = 0
                for item in products:
                    product_id = item['product']['id']
                    product_qty = item['qty']
                    product = Product.objects.get(id=product_id)
                    product_price = product.price
                    product_total_price = int(product_price) * int(product_qty)
                    total_price += product_total_price
                order = Order.objects.create(
                    title='Paid Order',
                    user = user,
                    total_price = total_price
                )
                order.save()
                for item in products:
                    product_id = item['product']['id']
                    product_qty = item['qty']
                    product = Product.objects.get(id=product_id)
                    product_price = product.price
                    product_total_price = int(product_price) * int(product_qty)
                    total_price += product_total_price
                    order_item = OrderItem.objects.create(
                        order=order,
                        product = product,
                        quantity = product_qty
                    )
                    order_item.save()
                order.is_paid = True
                order.save()
            return Response("Order Succesfully created", status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeliverOrderView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request, id, format=None):
        try:
            # user_id = request.user.id
            # user_usename = 'admin'
            # user = User.objects.get(id=user_id)

            if request.method == 'POST':
                order = Order.objects.get(id=id)
                if order.is_delivered == True:
                    return Response("This Order had already been delivereed", status=status.HTTP_400_BAD_REQUEST)
                order.is_delivered = True
                order.save()
                return Response("Order Succesfully Delivered", status=status.HTTP_201_CREATED)
        # except User.DoesNotExist:
        #     return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        except Order.DoesNotExist:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)