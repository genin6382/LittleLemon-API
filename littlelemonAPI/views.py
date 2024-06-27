# myapp/views.py
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view, permission_classes,throttle_classes
from rest_framework.response import Response
from rest_framework import status,generics
from .models import MenuItem,Category,Cart,Order,OrderItem
from .serializers import MenuItemSerializer,CategorySerializer,UserSerializer,CartSerializer,CartAddSerializer,OrderSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group,User
from datetime import date
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle,AnonRateThrottle])
def menu_item_list(request):
    menu_items = MenuItem.objects.all()
    if request.method == 'GET':
        category=request.query_params.get('category',None)
        price=request.query_params.get('price',None)
        search=request.query_params.get('search',None)
        featured=request.query_params.get('featured',None)
        ordering=request.query_params.get('ordering',None)
        perpage=request.query_params.get('perpage',default=8)
        page=request.query_params.get('page',default=1)

        if category:
            menu_items=MenuItem.objects.filter(category__title=category)
        if price:
            menu_items=MenuItem.objects.filter(price__lte=price)
        if search:
            menu_items=MenuItem.objects.filter(title__icontains=search)
        if featured is not None:
            if featured.lower()=='true':
                menu_items=MenuItem.objects.filter(featured=True)
            else:
                menu_items=MenuItem.objects.filter(featured=False)
        if ordering:
            menu_items=menu_items.order_by(ordering)

        paginator=Paginator(menu_items,per_page=perpage)
        try:
            menu_items=paginator.page(number=page)
        except PageNotAnInteger:
            menu_items=paginator.page(number=1)
        except EmptyPage:
            menu_items=[]

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
@throttle_classes([UserRateThrottle])
def category_list(request):
    if request.method == 'GET':
        category_items = Category.objects.all()
        title=request.query_params.get('title',None)
        perpage=request.query_params.get('perpage',default=5)
        page=request.query_params.get('page',default=1)

        if title:
            category_items=Category.objects.filter(title__iexact=title)

        paginator=Paginator(category_items,per_page=perpage)
        try:
            category_items=paginator.page(number=page)
        except PageNotAnInteger:
            category_items=paginator.page(number=1)
        except EmptyPage:
            category_items=[]
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
@throttle_classes([UserRateThrottle])
def menu_item_detail(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'GET':
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if not request.user.is_staff:
        return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PATCH':
        serializer = MenuItemSerializer(menu_item,data=request.data,partial=True)  #partial=True for update 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
@throttle_classes([UserRateThrottle])
def ListCreateManagerUser(request):
    if request.method=='GET':
        managers = User.objects.filter(groups__name="Manager")
        user=request.query_params.get('user',None)
        username=request.query_params.get('username',None)
        search=request.query_params.get('search',None)
        perpage=request.query_params.get('perpage',default=6)
        page=request.query_params.get('page',default=1)
        if user:
            managers=User.objects.filter(user__id=user)
        if username:
            managers=User.objects.filter(username__icontains=username)
        if search:
            managers=User.objects.filter(username__icontains=search)

        paginator=Paginator(managers,per_page=perpage)
        try:
            managers=paginator.page(number=page)
        except PageNotAnInteger:
            managers=paginator.page(number=1)
        except EmptyPage:
            managers=[]

        serializer=UserSerializer(managers,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method=="POST":
        managers=Group.objects.get(name="Manager")
        user=User.objects.get(username=request.data["username"])
        user.groups.add(managers)
        return Response(status=status.HTTP_201_CREATED)
    


@api_view(['GET','DELETE'])
@permission_classes([IsAdminUser])
@throttle_classes([UserRateThrottle])
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
@throttle_classes([UserRateThrottle])
def ListCreateDeliveryUser(request):
    if request.method=='GET':
        users=User.objects.filter(groups__name="Delivery_crew")

        user=request.query_params.get('user',None)
        username=request.query_params.get('username',None)
        search=request.query_params.get('search',None)
        perpage=request.query_params.get('perpage',default=5)
        page=request.query_params.get('page',default=1)
        if user:
            users=User.objects.filter(user__id=user)
        if username:
            users=User.objects.filter(username__icontains=username)
        if search:
            users=User.objects.filter(username__icontains=search)

        paginator=Paginator(users,per_page=perpage)
        try:
            users=paginator.page(number=page)
        except PageNotAnInteger:
            users=paginator.page(number=1)
        except EmptyPage:
            users=[]

        serializer=UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method=='POST':
        delivery_crew=Group.objects.get(name="Delivery_crew")
        user=User.objects.get(username=request.data["username"])
        user.groups.add(delivery_crew)
        return Response(status=status.HTTP_201_CREATED)
    
@api_view(['GET','DELETE'])
@permission_classes([IsAdminUser])
@throttle_classes([UserRateThrottle])
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
@throttle_classes([UserRateThrottle])
def ListCreateDeleteCart(request):
    user = request.user
    if request.method == 'GET':
        cart_items = Cart.objects.filter(user=user)
        search=request.query_params.get('search',None)
        price=request.query_params.get('price',None)
        ordering=request.query_params.get('ordering',None)
        perpage=request.query_params.get('perpage',default=6)
        page=request.query_params.get('page',default=1)
        if search:
            cart_items=Cart.objects.filter(menu_item__title__icontains=search)
        if price:
            cart_items=Cart.objects.filter(price__lte=price)
        if ordering:
            cart_items=cart_items.order_by(ordering)
        
        paginator=Paginator(cart_items,per_page=perpage)
        try:
            cart_items=paginator.page(number=page)
        except PageNotAnInteger:
            cart_items=paginator.page(number=1)
        except EmptyPage:
            cart_items=[]
    
        if cart_items:
            serializer = CartSerializer(cart_items, many=True)
            total_price = sum(item.price for item in cart_items)
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
@api_view(['GET','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def EditDeletCartItem(request,pk):
    cart_item = get_object_or_404(Cart, user=request.user, menu_item=pk)

    if not cart_item:
        return Response({"detail": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET' and cart_item.user==request.user:
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method=='PATCH' and cart_item.user==request.user:
        newdata=request.data
        serializer=CartAddSerializer(cart_item,data=newdata,partial=True)
        if serializer.is_valid():
            allowed_fields=["quantity"]
            for key in newdata.keys():
                if key not in allowed_fields:
                    return Response({"detail":"You are not authorized to update this field!"},status=status.HTTP_403_FORBIDDEN)
                
            new_quantity=newdata["quantity"]
            new_price=new_quantity*cart_item.menu_item.price
            serializer.save(quantity=new_quantity,price=new_price)
            total_price=sum([item.price for item in Cart.objects.filter(user=request.user)])

            return Response({"cart_item":serializer.data,"total_price":total_price},status=status.HTTP_200_OK)
    
    if request.method=='DELETE' and cart_item.user==request.user:
        cart_item.delete()
        return Response({"detail":"Item has been removed from cart."},status=status.HTTP_204_NO_CONTENT)
            

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])

def ListCreateOrder(request):

    if request.method=='GET':
        if request.user.groups.filter(name="Manager").exists():
            order=Order.objects.all()
        elif request.user.groups.filter(name="Delivery_crew").exists():
            order=Order.objects.filter(delivery_crew=request.user)
        else:
            order=Order.objects.filter(user=request.user)
        
        user=request.query_params.get('user',None)
        username=request.query_params.get('username',None)
        search=request.query_params.get('search',None)
        order_status=request.query_params.get('status',None)
        delivery_crew=request.query_params.get('delivery_crew',None)
        featured=request.query_params.get('featured',None)
        title=request.query_params.get('title',None)
        ordering=request.query_params.get('ordering',None)
        perpage=request.query_params.get('perpage',default=6)
        page=request.query_params.get('page',default=1)
        if user:
            order=Order.objects.filter(user__id=user)
        if username:
            order=Order.objects.filter(user__username__icontains=username)
        if search:
            order=Order.objects.filter(user__username__icontains=search)
        if order_status is not None:
            if order_status.lower()=="true":
                order=Order.objects.filter(status=True)
            else:
                order=Order.objects.filter(status=False)
        if delivery_crew:
            order=Order.objects.filter(delivery_crew__id=delivery_crew)
        if title:
            order=Order.objects.filter(order_items__menu_item__title__icontains=title)
        if featured:
            if featured.lower()=='true':
                order=Order.objects.filter(order_items__menu_item__featured=True)
            else:
                order=Order.objects.filter(order_items__menu_item__featured=False)
        if ordering:
            order=order.order_by(ordering)
        paginator=Paginator(order,per_page=perpage)

        try:
            order=paginator.page(number=page)
        except PageNotAnInteger:
            order=paginator.page(number=1)
        except EmptyPage:
            order=[]

        serializer=OrderSerializer(order,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    if request.method=='POST':

        cart_items=Cart.objects.filter(user=request.user)

        if request.user.groups.filter(name__in=["Manager","Delivery_crew"]).exists():
           return Response({"detail": "Not authorized to create orders."}, status=status.HTTP_403_FORBIDDEN)
        if not cart_items :
            return Response({"detail":"No items in cart to place an order."},status=status.HTTP_400_BAD_REQUEST)
        
        cart_item_dict={item.menu_item.title:item for item in cart_items}
        for order_item in request.data.get("order_items",[]):
            menu_item_title = order_item.get('menu_item')
            quantity = order_item.get('quantity')

            if menu_item_title not in cart_item_dict or quantity!=cart_item_dict[menu_item_title].quantity:
                return Response({"detail":"Invalid order item or quantity."},status=status.HTTP_400_BAD_REQUEST)

        total=sum([item.price for item in cart_items])
        order=Order.objects.create(user=request.user,status=False,total=total,date=date.today())
        for item in cart_items:
            OrderItem.objects.create(order=order,menu_item=item.menu_item,quantity=item.quantity,unit_price=item.unit_price,price=item.price)
            
        cart_items.delete()
        serializer=OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PATCH','PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def RetrieveUpdateDestroyOrder(request, pk):

    order=get_object_or_404(Order,id=pk)
    
    if request.method=='GET':
        if request.user.groups.filter(name="Manager") or request.user.groups.filter(name="Delivery_crew") and order.delivery_crew==request.user or order.user==request.user:
            serializer=OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not authorized to view this order."}, status=status.HTTP_403_FORBIDDEN)
        
    if request.method in ["PUT","PATCH"]:

        if request.user.groups.filter(name="Manager"):
            newdata=request.data
            allowed_fields=["status","delivery_crew"]

            for key in newdata.keys():
                if key not in allowed_fields:
                    return Response({"detail":"You are not authorized to update this field!"},status=status.HTTP_403_FORBIDDEN)
                
            serializer=OrderSerializer(order,data=newdata,partial=True)    #for patch and put - replacing old with new

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.user.groups.filter(name="Delivery_crew") and order.delivery_crew==request.user:
            newdata={"status":request.data["status"]}

            allowed_fields=["status"]
            for key in newdata.keys():
                if key not in allowed_fields:
                    return Response({"detail":"You are not authorized to update this field!"},status=status.HTTP_403_FORBIDDEN)
                
            serializer=OrderSerializer(order,data=newdata,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    if request.method=="DELETE":
        if request.user.groups.filter(name="Manager") or request.user==order.user:
            order.delete()
            return Response({"Detail":"This order has been deleted successfully!"},status=status.HTTP_204_NO_CONTENT)
        
        return Response({"detail": "Not authorized to perform this Operation !."}, status=status.HTTP_403_FORBIDDEN)
        





