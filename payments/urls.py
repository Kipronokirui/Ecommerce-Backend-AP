from django.urls import path
from . import views 

urlpatterns=[
    path("orders/", views.OrdersList.as_view(), name='orders'),
    path("checkout/", views.CreateOrderView.as_view(), name='checkout'),
    path("dashboard/orders/", views.UserOrdersView.as_view(), name='user_orders'),
    path("order/<int:id>/", views.DeliverOrderView.as_view(), name='deliver_order'),
]