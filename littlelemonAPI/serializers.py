from rest_framework import serializers
from .models import MenuItem,Category,Cart,Order,OrderItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='title'
    )

    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category']
        extra_kwargs={'price':{'min_value':10}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class CartSerializer(serializers.ModelSerializer):
    menu_item=MenuItemSerializer()
    class Meta:
        model=Cart
        fields=['menu_item','quantity','price']
        extra_kwargs={'quantity':{'min_value':1}}

class CartAddSerializer(serializers.ModelSerializer):
    menu_item = serializers.CharField()

    class Meta:
        model = Cart
        fields = ['menu_item', 'quantity']
        extra_kwargs = {'quantity': {'min_value': 1}}

    def validate_menu_item(self, value):
        try:
            menu_item = MenuItem.objects.get(title=value)
        except MenuItem.DoesNotExist:
            raise serializers.ValidationError(f"Menu item with title '{value}' does not exist.")
        return menu_item

    def create(self, validated_data):
        menu_item = validated_data.pop('menu_item')
        user = self.context['request'].user
        quantity = validated_data['quantity']
        price = quantity * menu_item.price
        cart_item = Cart.objects.create(user=user, menu_item=menu_item, quantity=quantity, unit_price=menu_item.price, price=price)
        return cart_item


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item=MenuItemSerializer()
    class Meta:
        model=OrderItem
        fields=['id', 'menu_item', 'quantity', 'unit_price', 'price']
        

class OrderSerializer(serializers.ModelSerializer):
    user =serializers.SerializerMethodField()
    order_items = OrderItemSerializer(many=True, read_only=True) 
    delivery_crew = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Order
        fields = ['id', 'user','date','order_items','total','status','delivery_crew']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime('%Y-%m-%d')  
        return representation

    def get_user(self,obj):
        return obj.user.username