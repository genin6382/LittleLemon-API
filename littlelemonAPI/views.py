# myapp/views.py
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status,generics
from .models import MenuItem,Category,Cart,Order,OrderItem
from .serializers import MenuItemSerializer,CategorySerializer,UserSerializer,CartSerializer,CartAddSerializer,OrderItemSerializer,OrderSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group,User
from datetime import date

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])

def menu_item_list(request):
    menu_items = MenuItem.objects.all()
    if request.method == 'GET':
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        if request.user.is_staff:
            serializer = MenuItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        if request.user.is_staff:
            MenuItem.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def category_list(request):
    if request.method == 'GET':
        category_items = Category.objects.all()
        serializer = CategorySerializer(category_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def menu_item_detail(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'GET':
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if not request.user.is_staff:
        return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PATCH':
        serializer = MenuItemSerializer(data=request.data,partial=True)  #partial=True for update 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def ListCreateManagerUser(request):
    if request.method=='GET':
        managers = User.objects.filter(groups__name="Manager")
        serializer=UserSerializer(managers,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method=="POST":
        managers=Group.objects.get(name="Manager")
        user=User.objects.get(username=request.data["username"])
        user.groups.add(managers)
        return Response(status=status.HTTP_201_CREATED)
    


@api_view(['GET','DELETE'])
@permission_classes([IsAdminUser])
def RemoveManagerUser(request,pk):
    if pk:
        user=User.objects.get(pk=pk)
        serializer=UserSerializer(user)
        managers=Group.objects.get(name="Manager")
        user.groups.remove(managers)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST'])
@permission_classes([IsAdminUser])

def ListCreateDeliveryUser(request):
    if request.method=='GET':
        users=User.objects.filter(groups__name="Delivery_crew")
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method=='POST':
        delivery_crew=Group.objects.get(name="Delivery_crew")
        user=User.objects.get(username=request.data["username"])
        user.groups.add(delivery_crew)
        return Response(status=status.HTTP_201_CREATED)
    
@api_view(['GET','DELETE'])
@permission_classes([IsAdminUser])
def RemoveDeliveryUser(request,pk):
    if pk:
        user=User.objects.get(pk=pk)
        serializer=UserSerializer(user)
        delivery_crew=Group.objects.get(name="Delivery_crew")
        user.groups.remove(delivery_crew)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])

def ListCreateDeleteCart(request):
    user = request.user
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user=user)
        if cart_items.exists():
            serializer = CartSerializer(cart_items, many=True)
            total_price=0
            for item in cart_items:
                total_price+=item.price
            return Response({"cart_items":serializer.data,"total_price":total_price}, status=status.HTTP_200_OK)
        return Response({"Message": "No items found in your cart!"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        data = request.data.copy()
        serializer = CartAddSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        cart_items = Cart.objects.filter(user=user)
        cart_items.delete()
        return Response({"Message": "All items have been deleted. Cart is empty."}, status=status.HTTP_204_NO_CONTENT)
    
#ADD A FUNCTIONALITY TO REMOVE SOME ITEMS FROM THE CART , BY REDUCING THE QUANTITY BY THE CART FROM THE NUMBER OBTAINED IN FORM

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def ListCreateOrder(request):

    if request.method=='GET':
        if request.user.groups.filter(name="Manager").exists():
            orders=Order.objects.all()
        elif request.user.groups.filter(name="Delivery_crew").exists():
            order=Order.objects.filter(delivery_crew=request.user)
        else:
            order=Order.objects.filter(user=request.user)

        serializer=OrderSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    if request.method=='POST':

        cart_items=Cart.objects.filter(user=request.user)

        if request.user.groups.filter(group__name__in=["Manager","Delivery_crew"]).exists():
           return Response({"detail": "Not authorized to create orders."}, status=status.HTTP_403_FORBIDDEN)
        if not cart_items :
            return Response({"detail":"No items in cart to place an order."},status=status.HTTP_400_BAD_REQUEST)
        
        total=sum([item.price for item in cart_items])
        cart_items["total_price"]=total
        order=Order.objects.create(user=request.user,status=False,total=total,data=date.today())
        for item in cart_items:
            OrderItem.objects.create(order=order,menu_item=item.menu_item,quantity=item.quantity,unit_price=item.unit_price,price=item.price)
            
        cart_items.delete()
        serializer=OrderSerializer(order,many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PATCH','PUT', 'DELETE'])
def RetrieveUpdateDestroyOrder(request, pk):

    order=get_object_or_404(Order,pk=pk)
    
    if request.method=='GET':
        if request.user.groups.filter(group__name="Manager") or request.user.groups.filter(group__name="Delivery_crew") and order.delivery_crew==request.user or order.user==request.user:
            serializer=OrderSerializer(order,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not authorized to view this order."}, status=status.HTTP_403_FORBIDDEN)
        
    if request.method in ["PUT","PATCH"]:
        if request.user.groups.filter(group__name="Manager"):
            newdata=request.data
            serializer=OrderSerializer(order,data=newdata,partial=True)    #for patch and put - replacing old with new
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.user.groups.filter(group__name="Delivery_crew") and order.delivery_crew==request.user:
            newdata={"status":request.data["status"]}
            serializer=OrderSerializer(order,data=newdata,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.user==order.user:
            newdata=request.data
            if 'status' and 'delivery_crew' in newdata:
                return Response({"detail":"You are not authorized for updating status or delivery crew!"},status=status.HTTP_403_FORBIDDEN)
            
            serializer=OrderSerializer(order,data=newdata,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    if request.method=="DELETE":
        if request.user.groups.filter(group__name="Manager"):
            order.delete()
            return Response({"Detail":"This order has been deleted successfully!"},status=status.HTTP_204_NO_CONTENT)
        
        return Response({"detail": "Not authorized to perform this Operation !."}, status=status.HTTP_403_FORBIDDEN)
        





