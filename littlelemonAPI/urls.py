from django.urls import path
from . import views

urlpatterns = [
    # Menu-items endpoints
    path('menu-items/', views.menu_item_list,name='menu_item_list'),
    path('menu-items/category', views.category_list,name='category_list'),
    path('menu-items/<int:pk>', views.menu_item_detail,name='menu_item_detail'),

    #user group management endpoints
    path('groups/manager/users',views.ListCreateManagerUser,name='manager_user_list'),
    path('groups/manager/users/<int:pk>',views.RemoveManagerUser,name='manager_user_remove'),
    path('groups/delivery-crew/users',views.ListCreateDeliveryUser,name='delivery_user_list'),
    path('groups/delivery-crew/users/<int:pk>',views.RemoveDeliveryUser,name='delivery_user_remove'),
    
    #Cart management endpoints
    path('cart/menu-items',views.ListCreateDeleteCart,name='cart_list'),
    path('cart/menu-items/<int:pk>',views.EditDeletCartItem,name='cart_detail'),

    #Order management endpoints
    path('orders/',views.ListCreateOrder,name='order_list'),
    path('orders/<int:pk>',views.RetrieveUpdateDestroyOrder,name='order_detail'),
    
]
