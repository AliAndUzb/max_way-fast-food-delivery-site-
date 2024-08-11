from contextlib import closing
from django.db import connection
from food.models import OrderProduct


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_table():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT food_orderproduct.product_id,COUNT(food_orderproduct.product_id),food_product.title
        FROM food_orderproduct 
        INNER JOIN food_product ON food_product.id=food_orderproduct.product_id
        GROUP BY food_orderproduct.product_id, food_product.title
        ORDER BY COUNT DESC LIMIT 10;
        """)
        table = dictfetchall(cursor)
        return table


def get_order_by_user(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT food_order.id, food_customer.first_name, food_customer.last_name, food_order.status,
        food_order.created_at, food_order.address, food_order.payment_type FROM food_order 
        INNER JOIN food_customer ON food_order.customer_id=food_customer.id
        WHERE food_order.customer_id=%s""", [id])
        user = dictfetchall(cursor)
        return user


# def get_product_by_order(id):
#     with closing(connection.cursor()) as cursor:
#         cursor.execute("""SELECT food_orderproduct.price, food_orderproduct.count, food_orderproduct.created_at,
#         food_product.title FROM food_orderproduct
#         INNER JOIN food_product ON food_orderproduct.product_id=food_product.id
#         WHERE food_order.id = %s""", [id])
#         order_product = dictfetchall(cursor)
#
#         return order_product


# def get_product_by_order(id):
#     # Assuming you have a foreign key from OrderProduct to Order as 'order'
#     order_products = OrderProduct.objects.filter(order_id=id).select_related('product').values(
#         'price',
#         'count',
#         'created_at',
#         'product__title'
#     )
#
#     return list(order_products)


def get_product_by_order(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(""" SELECT food_orderproduct.count,food_orderproduct.price,
        food_orderproduct.created_at,food_product.title from food_orderproduct 
         INNER JOIN food_product ON food_orderproduct.product_id=food_product.id  where order_id=%s""",[id])
        orderproduct = dictfetchall(cursor)
        return orderproduct