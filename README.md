# Little Lemon API

The Little Lemon API is an API for the Little Lemon restaurant. Little Lemon's management wants to have an online-based order management system and mobile application. The LittleLemonAPI is the back-end API that allows customers to browse food items, view the item of the day and place orders. Managers are able to update the item of the day and monitor orders and assign deliveries.  The delivery crew are able to check the orders assigned to them and update an order once it is delivered.

## Features

User groups
It contains two user groups (Manager & Delivery crew) and some random users assigned to these groups from the Django admin panel.

 Manager

Delivery crew

Users not assigned to a group will be considered customers.

This API makes it possible end-users to perform certain tasks. It has the following functionalities.

1.	The admin can assign users to the manager group

2.	You can access the manager group with an admin token

3.	The admin can add menu items 

4.	The admin can add categories

5.	Managers can log in 

6.	Managers can update the item of the day

7.	Managers can assign users to the delivery crew

8.	Managers can assign orders to the delivery crew

9.	The delivery crew can access orders assigned to them

10.	The delivery crew can update an order as delivered

11.	Customers can register

12.	Customers can log in using their username and password and get access tokens

13.	Customers can browse all categories 

14.	Customers can browse all the menu items at once

15.	Customers can browse menu items by category

16.	Customers can paginate menu items

17.	Customers can sort menu items by price

18.	Customers can add menu items to the cart

19.	Customers can access previously added items in the cart

20.	Customers can edit their cart

21.	Customers can remove items from the cart

22.	Customers can place orders

23.	Customers can browse their own orders

# API STRUCTURE

## /api/menu-items/

     
    -GET method:
        ACCPETS PARAMS: ?perpage=5-50 | ?page=1 | ?search=title  | ?price=number  |  ?category=category_name | ?featured=true/false | (acsending order)?ordering=price | (decending order)?ordering=-price
        -from Anonomous:
            displays menu items rate limit set at 5 per day
        -from Users and Managers and Superuser:
            displays menu items rate limit set at 400 per day
    -POST method:
        -from Superusers
            Creates menu item when given data:
                title
                price
                featured
                category

## /api/menu-items/category

    ACCPETS PARAMS: ?perpage=5-50 | ?page=1 | ?title=title | 
    -GET method:
        From Superusers:
            Lists all menu item categories
    -POST method:
        From Superusers:
            Adds a category given:
                slug
                title

## /api/menu-items/{menuitemId}

    -GET method:
        Displays all details of the given {menuitemId} 
    -PATCH method:
        from Managers and Superusers:
            Toggles the featured status of the given {menuitemId}
            Can Change the price of the given {menuitemId}
    -DELETE method:
        from Superusers:
            Deletes the given {menuitemId}

## /api/groups/managers/users
     ACCPETS PARAMS: ?perpage=5-50 | ?page=1 | ?search=username  | ?username=username  | ?user=user_id 
    -GET method:
        -from Managers and Superusers:
            Lists all users in the managers group
    -POST method:
        -from Managers and Superusers:
            Adds a user to the managers group given:
                username
                email

## /api/groups/managers/users/{userId}

    -DELETE method:
        from Managers and Superusers:
            Removes the User associated with {userId} from the managers group 

## /api/groups/delivery-crew/users
    ACCPETS PARAMS: ?perpage=5-50 | ?page=1 | ?search=username  | ?username=username  | ?user=user_id 
    
    -GET method:
        -from Managers and Superusers:
            Lists all users in the delivery crew group
    -POST method:
        -from Managers and Superusers:
            Adds a user to the delivery crew group given:
                username
                email

## /api/groups/delivery-crew/users/{userId}

    -DELETE method:
        from Managers and Superusers:
            Removes the User associated with {userId} from the delivery crew group

## /api/cart/menu-items
    ACCPETS PARAMS: ?perpage=5-50 | ?page=1 | ?search=menu_item_title  | ?price=number | (acsending order)?ordering=price | (decending order)?ordering=-price
    -GET method:
        from Users:
            Displays all items and quantities currently in user's cart
    -POST method:
        from Users:
            Adds a menu item to the user's cart given:
                order_items: An array of objects representing the menu items to be added to the cart. Each object includes:
                      menu_item: The name or ID of the menu item to add.
                      quantity: The quantity of the menu item to add to the cart.
     -DELETE method:
        from Users:
           removes all items from cart


## /api/cart/menu-items/{menuitemId}

    -GET method:
        from Users:
            Displays the particular menu item in the cart
    -PATCH method:
        from Users:
            Modify the quantity of the given menu item in the user's cart, given:
                quantity
    -DELETE method:
        from Users:
            removes the given menuitem from the cart

## /api/orders
    ACCPETS PARAMS: ?perpage=5-50 | ?page=1 | ?search=user_username  | ?title=order_items_menu_item_title | ?featured=true/false | ?delivery_crew=delivery_crew_id | ?order_status=true/false | ?user=user_id | ? 
                     username=user_username (acsending order)?ordering=price  | (decending order)?ordering=-price
    -GET method:
        from Users:
            Displays orders owned by user
        from Delivery Crew:
            Displays orders assigned to delivery crew member
        from Managers and Superusers:
            Displays all orders
    -POST method:
        places an order based on items in the user's cart, and empties the cart.

## /api/orders/{orderId}

    -GET method:
        from User:
            Shows the order details associated with {orderId} details if user is owner of order.
        from Delivery crew, Managers and Superusers:
            Shows the order details associated with {orderId}
    -PATCH method:
        from from Delivery crew, Managers and Superusers:
            Toggles the status of the order associated with {orderId}
    -PUT method:
        from Managers and Superusers:
            Assigns a delivery crew to the the order associated with {orderId}
    -DELETE method:
        from Managers and Superusers:
            Deletes the order associated with {orderId}



## /api/auth/users

    -GET method: 
        -from Anonomous:
            401 - unauthorized
        -from registered User and Manager:
            Retrieves requesting user information
        -from Superuser:
            Retrieves all Users information

## /api/auth/users/

    -POST method:
        Allows everyone to register an account when supplied with the data:
            username
            password
            email  
               
## /api/auth/token/login/

    -POST method:
        Returns authorization token for given login:
            username
            password 

## /api/auth/users/me

    -GET method:
        displays user information based on token
        NOTE a user token is required for all features of the API with the exception of registering and viewing the menu


       
